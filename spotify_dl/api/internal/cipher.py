import logging
import struct

from spotify_dl.utils.crypto import Shannon
from spotify_dl.utils.connection import SocketConnection
from spotify_dl.api.internal.packet import Packet, PacketType



class CipherPair:
    logger: logging.Logger = logging.getLogger("spdl:cipher")

    def __init__(self, send_key: bytes, receive_key: bytes) -> None:
        self.send_cipher: Shannon = Shannon()
        self.send_cipher.key(send_key)
        self.recv_cipher: Shannon = Shannon()
        self.recv_cipher.key(receive_key)

        self.send_nonce: int = 0
        self.recv_nonce: int = 0

    def send_encoded(self, conn: SocketConnection, cmd: bytes, payload: bytes) -> None:
        self.send_cipher.nonce(self.send_nonce)
        self.send_nonce += 1

        conn.write(cmd)
        conn.write_sized(len(payload), "u16")
        conn.write(payload)

        content = self.send_cipher.encrypt(conn.copy_buf())
        mac = self.send_cipher.finish(4)

        conn.clear_buf()
        conn.write(content)
        conn.write(mac)
        conn.flush()

    def recv_encoded(self, conn: SocketConnection) -> Packet:
        try:
            self.recv_cipher.nonce(self.recv_nonce)
            self.recv_nonce += 1

            a = conn.read(3)
            header_bytes = self.recv_cipher.decrypt(a)

            cmd = struct.pack(">s", bytes([header_bytes[0]]))
            self.logger.debug(f"CMD_TYPE={PacketType.get_name(cmd)}")
            payload_length = (header_bytes[1] << 8) | (header_bytes[2] & 0xFF)

            payload_bytes = self.recv_cipher.decrypt(conn.read(payload_length))

            mac = conn.read(4)
            expected_mac = self.recv_cipher.finish(4)
            if mac != expected_mac:
                raise RuntimeError()

            return Packet(cmd, payload_bytes)
        except IndexError:
            raise RuntimeError("Failed to receive packet")
