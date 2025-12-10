import struct
from typing import final
from spotify_dl.api.internal.spotify_client import SpotifyClient
from spotify_dl.api.internal.proto.mercury_pb2 import Header


# TOOD: using plain shannon channel doesnt work, maybe using mercury works?
@final
class Mercury:
    def __init__(self, client: SpotifyClient) -> None:
        self.client = client

    def send(
        self,
        uri: str,
        method: bytes,
    ) -> None:
        if not self.client.cipher:
            raise ValueError("cipher is not initialized, is the handshake successful?")

        buf = bytearray()
        buf.extend(struct.pack(">HQBH", 8, self.client.seq, 1, 1))
        self.client.seq += 1

        header = Header(
            uri=uri,
            method=method.decode(),
        )

        header_buf = header.SerializeToString()
        buf.extend(struct.pack(">H", len(header_buf)))
        buf.extend(header_buf)

        self.client.cipher.send_encoded(
            self.client.conn,
            method,
            bytes(buf),
        )
