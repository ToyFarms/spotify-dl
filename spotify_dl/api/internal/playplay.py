import binascii
from spotify_dl.auth.clienttoken import ClientToken
from spotify_dl.auth.login5 import Login5Auth
from spotify_dl.key_provider import KeyProvider
from spotify_dl.api.internal.proto.playplay_pb2 import (
    AUDIO_TRACK,
    DOWNLOAD,
    INTERACTIVE,
    PlayPlayLicenseRequest,
    PlayPlayLicenseResponse,
)
from spotify_dl.api.web.apresolve import get_random_spclient
from spotify_dl.playplay.playplay_c import playplay_decrypt


class PlayPlay(KeyProvider):
    # TODO: re the token, if its still even using playplay
    PLAYPLAY_TOKEN: bytes = b"\x01\xe12\xca\xe5'\xbd!b\x0e\x82/XQI2"

    def __init__(self, auth: Login5Auth, clienttoken: ClientToken) -> None:
        self.auth: Login5Auth = auth
        self.clienttoken: ClientToken = clienttoken

    def get_audio_key(self, gid: bytes, file_id: bytes) -> bytes | None:
        req = PlayPlayLicenseRequest(
            version=2,
            token=bytes(PlayPlay.PLAYPLAY_TOKEN),
            interactivity=INTERACTIVE,
            content_type=AUDIO_TRACK,
        )

        resp = self.auth.session.post(
            f"https://spclient.wg.spotify.com/playplay/v1/key/{file_id.hex()}",
            headers={
                "Content-Type": "application/x-protobuf",
                "Accept": "*/*",
                "client-token": self.clienttoken.token,
            },
            data=req.SerializeToString(),
        )
        resp.raise_for_status()

        res = PlayPlayLicenseResponse()
        _ = res.FromString(resp.content)

        return playplay_decrypt(res.obfuscated_key, file_id)
