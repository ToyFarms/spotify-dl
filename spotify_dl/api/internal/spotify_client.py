import base64
import io
import logging
import os
import socket
import struct
import time
import uuid

from typing import Self, TypeGuard, cast, TypedDict, override
from Cryptodome.Hash import HMAC, SHA1
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5

from spotify_dl.auth.auth_provider import AuthProvider
from spotify_dl.auth.web_auth import SpotifyAuthPKCE
from spotify_dl.key_provider import KeyProvider
from spotify_dl.api.web.apresolve import get_accesspoint
from spotify_dl.utils.connection import SocketConnection
from spotify_dl.utils.crypto import DHKey
from spotify_dl.api.internal.cipher import CipherPair
from spotify_dl.api.internal.packet import PacketType
from spotify_dl.api.internal.proto.keyexchange_pb2 import (
    APLoginFailed,
    APResponseMessage,
    ClientHello,
    BuildInfo,
    ClientResponsePlaintext,
    CryptoResponseUnion,
    LoginCryptoDiffieHellmanResponse,
    LoginCryptoResponseUnion,
    PoWResponseUnion,
    Product,
    ProductFlags,
    Platform,
    Cryptosuite,
    LoginCryptoHelloUnion,
    LoginCryptoDiffieHellmanHello,
)
from spotify_dl.api.internal.proto.authentication_pb2 import (
    APWelcome,
    AuthenticationType,
    ClientResponseEncrypted,
    CpuFamily,
    LoginCredentials,
    Os,
    SystemInfo,
)
from spotify_dl.utils.misc import random_order


class ReusableSchema(TypedDict):
    username: str
    credentials: str


class SpotifyClient(AuthProvider[ReusableSchema], KeyProvider):
    logger: logging.Logger = logging.getLogger("spdl:client")

    SERVER_KEY: int = (
        21823581898349655569073153010024875866680360595041832877682009086525543062007759377936242326561802478825880089458110335403551375236649157065502301012891458399825664119417150281976229148711139317450628328839720892460534096843275538011418744806604964798210621296650510908306523427425696959525181094419017879246106872673711968985492349600443051010137641078005441820342625510004834802242062196525075763597088556647911324288377975942408884781721344719415751475652337673266953113087580192529673091473125075313299523391491535787804999014442523894945078938686301787840555533712734909924635503633011364796383888738282283357629
    )
    Auth: type[AuthenticationType] = AuthenticationType

    def __init__(
        self,
        addr: str,
        port: int,
        auth: SpotifyAuthPKCE,
    ) -> None:
        super().__init__(key="spclient")
        self.addr: str = addr
        self.port: int = port
        self.auth: SpotifyAuthPKCE = auth
        self.conn: SocketConnection = SocketConnection(addr, port)
        self.device_id: str = str(uuid.uuid4())

        self.key: DHKey = DHKey()
        self.seq: int = 0

        self.cipher: CipherPair | None = None
        self.authenticated: bool = False

    @property
    @override
    def token(self) -> str:
        if not self.is_token_valid(self._token):
            if self.authenticated:
                self.refresh_token()
            else:
                self.handshake()
                self.authenticate_with_token()

        if not self._token:
            raise

        return self._token["credentials"]

    @property
    def reusable(self) -> ReusableSchema:
        if not self.is_token_valid(self._token):
            if self.authenticated:
                self.refresh_token()
            else:
                self.handshake()
                self.authenticate_with_token()

        if not self._token:
            raise

        return self._token

    @override
    def is_token_expired(self, token: ReusableSchema | None = None) -> bool:
        token = token or self._token
        return not token

    @override
    def is_token_valid(
        self, token: ReusableSchema | None = None
    ) -> TypeGuard[ReusableSchema]:
        token = token or self._token
        return bool(token and token["credentials"] and token["username"])

    @override
    def refresh_token(self) -> None:
        self.conn.close()
        self._save(None)
        self.cipher = None

        aps = get_accesspoint()
        connected = False
        for addr, port in random_order(aps):
            try:
                self.conn = SocketConnection(addr, port)
                self.addr = addr
                self.port = port
                connected = True
                break
            except ConnectionRefusedError:
                time.sleep(0.5)

        if not connected:
            raise ConnectionRefusedError("Could not reconnect to spotify server")

        self.handshake()
        self.authenticate_with_token()

    @classmethod
    def connect_retry(
        cls, addr: str, port: int, auth: SpotifyAuthPKCE, max_retry: int = 5
    ) -> Self | None:
        for _ in range(max_retry, 0, -1):
            try:
                return cls(addr, port, auth)
            except ConnectionRefusedError:
                time.sleep(0.5)

    @classmethod
    def random_ap(cls, auth: SpotifyAuthPKCE) -> Self:
        aps = get_accesspoint()
        for addr, port in random_order(aps):
            client = cls.connect_retry(addr, port, auth)
            if client:
                return client

        raise ConnectionRefusedError("Tried all ap's 5 TIMES still didn't work")

    def handshake(self) -> None:
        acc = bytearray()

        hello = ClientHello(
            build_info=BuildInfo(
                product=Product.PRODUCT_CLIENT,
                product_flags=[ProductFlags.PRODUCT_FLAG_NONE],
                platform=Platform.PLATFORM_LINUX_X86,
                version=117300517,
            ),
            client_nonce=os.urandom(0x10),
            cryptosuites_supported=[Cryptosuite.CRYPTO_SUITE_SHANNON],
            login_crypto_hello=LoginCryptoHelloUnion(
                diffie_hellman=LoginCryptoDiffieHellmanHello(
                    gc=self.key.public_bytes, server_keys_known=1
                ),
            ),
            padding=b"\x1e",
        )

        hello_bytes = hello.SerializeToString()

        self.conn.write(b"\x00\x04")
        self.conn.write_sized(len(hello_bytes) + 2 + 4, "i32")
        self.conn.write(hello_bytes)
        acc.extend(self.conn.copy_buf())

        self.conn.flush()

        size = self.conn.read_sized("i32")
        resp = self.conn.read(size - 4)

        acc.extend(size.to_bytes(4))
        acc.extend(resp)

        resp_packet = APResponseMessage()
        _ = resp_packet.ParseFromString(resp)

        if resp_packet.login_failed.error_code:
            self.logger.fatal(
                f"LOGIN FAILED: {resp_packet.login_failed.error_code}, REASON: {resp_packet.login_failed.error_description}"
            )
            raise

        shared_key = self.key.shared_key(
            resp_packet.challenge.login_crypto_challenge.diffie_hellman.gs
        )

        rsa = RSA.construct((self.SERVER_KEY, 65537))
        pkcs1_v1_5 = PKCS1_v1_5.new(rsa)
        sha1 = SHA1.new()
        sha1.update(resp_packet.challenge.login_crypto_challenge.diffie_hellman.gs)
        if not pkcs1_v1_5.verify(
            sha1,
            resp_packet.challenge.login_crypto_challenge.diffie_hellman.gs_signature,
        ):
            raise RuntimeError("Failed signature check!")

        buffer = io.BytesIO()
        for i in range(1, 6):
            mac = HMAC.new(shared_key, digestmod=SHA1)
            _ = mac.update(acc)
            _ = mac.update(bytes([i]))
            _ = buffer.write(mac.digest())

        _ = buffer.seek(0)
        mac = HMAC.new(buffer.read(20), digestmod=SHA1)
        _ = mac.update(acc)
        challenge = mac.digest()
        client_resp = ClientResponsePlaintext(
            crypto_response=CryptoResponseUnion(),
            login_crypto_response=LoginCryptoResponseUnion(
                diffie_hellman=LoginCryptoDiffieHellmanResponse(hmac=challenge)
            ),
            pow_response=PoWResponseUnion(),
        )

        client_resp_bytes = client_resp.SerializeToString()
        self.conn.write_sized(len(client_resp_bytes) + 4, "i32")
        self.conn.write(client_resp_bytes)
        self.conn.flush()

        try:
            self.conn.set_timeout(1)
            scrap = self.conn.read(4)
            if len(scrap) == 4:
                payload = self.conn.read(cast(int, struct.unpack(">i", scrap)[0] - 4))
                failed = APResponseMessage()
                _ = failed.ParseFromString(payload)
                raise RuntimeError(failed)
        except socket.timeout:
            pass
        finally:
            self.conn.set_timeout(0)

        _ = buffer.seek(20)
        self.cipher = CipherPair(buffer.read(32), buffer.read(32))

        self.logger.info(f"SUCCESSFULLY CONNECTED")

    def authenticate(self) -> None:
        if self.is_token_valid():
            self.authenticate_with_reusable()
        else:
            self.authenticate_with_token()

    def authenticate_with_token(self) -> None:
        self._authenticate(
            None,
            self.auth.token.encode("utf-8"),
            AuthenticationType.AUTHENTICATION_SPOTIFY_TOKEN,
        )

    def authenticate_with_reusable(self) -> None:
        if not self.is_token_valid():
            self.authenticate_with_token()
            return

        self._authenticate(
            self.reusable["username"],
            base64.b64decode(self.reusable["credentials"].encode("utf-8")),
            AuthenticationType.AUTHENTICATION_STORED_SPOTIFY_CREDENTIALS,
        )

    def _authenticate(
        self,
        username: str | None,
        credentials: bytes,
        type: AuthenticationType,
    ) -> None:
        if not self.cipher:
            raise ValueError("cipher is not initialized, is the handshake successful?")

        resp = ClientResponseEncrypted(
            login_credentials=LoginCredentials(
                username=username,
                auth_data=credentials,
                typ=type,
            ),
            system_info=SystemInfo(
                cpu_family=CpuFamily.CPU_UNKNOWN,
                os=Os.OS_UNKNOWN,
                system_information_string="libspot",
                device_id=self.device_id,
            ),
            version_string="0.0.1",
        )

        self.cipher.send_encoded(self.conn, PacketType.login, resp.SerializeToString())
        packet = self.cipher.recv_encoded(self.conn)

        if packet.type == PacketType.ap_welcome:
            self.logger.info("AUTHENTICATED")

            ap_welcome = APWelcome()
            _ = ap_welcome.ParseFromString(packet.payload)

            self._save(
                {
                    "username": ap_welcome.canonical_username,
                    "credentials": base64.b64encode(
                        ap_welcome.reusable_auth_credentials
                    ).decode(),
                }
            )
            self.authenticated = True
        elif packet.type == PacketType.auth_failure:
            login_failed = APLoginFailed()
            _ = login_failed.ParseFromString(packet.payload)
            raise RuntimeError(login_failed)
        else:
            raise RuntimeError(f"Unknown CMD {PacketType.get_name(packet.type)}")

    @override
    def get_audio_key(self, gid: bytes, file_id: bytes) -> bytes | None:
        if not self.cipher:
            raise ValueError("cipher is not initialized, is the handshake successful?")

        buf = bytearray()
        buf.extend(file_id)
        buf.extend(gid)
        buf.extend(struct.pack(">I", self.seq))
        buf.extend(b"\x00\x00")
        self.seq += 1

        self.cipher.send_encoded(self.conn, PacketType.request_key, bytes(buf))

        while True:
            packet = self.cipher.recv_encoded(self.conn)
            self.logger.debug(packet)

            if packet.type in (PacketType.aes_key, PacketType.aes_key_error):
                payload = io.BytesIO(packet.payload)
                seq = cast(int, struct.unpack(">i", payload.read(4))[0])
                self.logger.debug(f"SEQ: {seq}")
                if packet.type == PacketType.aes_key:
                    return payload.read(16)
                elif packet.type == PacketType.aes_key_error:
                    code = cast(int, struct.unpack(">H", payload.read(2))[0])
                    self.logger.error(
                        f"Failed to get aes key, code: {code}. Track codec possibly gated behind premium user, continuing without a key (encrypted)"
                    )
                    return
            else:
                if packet.type == PacketType.ping:
                    self.cipher.send_encoded(
                        self.conn,
                        PacketType.pong,
                        b"\x00\x00\x00\x00",
                    )
