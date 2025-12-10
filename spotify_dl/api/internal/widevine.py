# pyright: basic

from pathlib import Path
from typing import cast, override
from pywidevine.cdm import Cdm
from pywidevine.device import Device
from pywidevine.pssh import PSSH
import curl_cffi

from spotify_dl.api.web.apresolve import get_random_spclient
from spotify_dl.auth.clienttoken import ClientToken
from spotify_dl.key_provider import KeyProvider
from spotify_dl.auth.internal_auth import SpotifyInternalAuth


class WidevineClient(KeyProvider):
    def __init__(
        self,
        iauth: SpotifyInternalAuth,
        clienttoken: ClientToken,
        widevine_license: Path | str,
    ) -> None:
        if iauth.is_linked_with_account() is None:
            iauth.authenticate()

        if not iauth.is_linked_with_account():
            raise RuntimeError(
                "token cannot be anonymous when using widevine, did you pass sp_dc to iauth?"
            )

        self.iauth: SpotifyInternalAuth = iauth
        self.clienttoken: ClientToken = clienttoken

        self.device: Device = Device.load(widevine_license)
        self.cdm: Cdm = Cdm.from_device(self.device)

        self.session: bytes = self.cdm.open()

    @override
    def get_audio_key(self, gid: bytes, file_id: bytes) -> bytes | None:
        pssh = PSSH(
            cast(
                str,
                curl_cffi.get(
                    f"https://seektables.scdn.co/seektable/{file_id.decode()}.json",
                    impersonate="chrome",
                ).json()["pssh"],
            )
        )

        challenge = self.cdm.get_license_challenge(
            self.session,
            pssh,
            license_type="STREAMING",
            privacy_mode=False,
        )

        license = curl_cffi.post(
            f"https://{get_random_spclient()[0]}/widevine-license/v1/audio/license",
            data=challenge,
            headers={
                "Authorization": f"Bearer {self.iauth.token}",
                "Client-Token": self.clienttoken.token,
            },
            impersonate="chrome",
        )
        license.raise_for_status()

        self.cdm.parse_license(self.session, license.content)

        keys = self.cdm.get_keys(self.session)
        ret: list[bytes] = []

        for key in keys:
            if key.type.lower() != "content":
                continue

            ret.append(f"{key.kid.hex}:{key.key.hex()}".encode())

        return b" ".join(ret)


if __name__ == "__main__":
    pass
