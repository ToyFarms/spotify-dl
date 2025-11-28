from pathlib import Path
import pickle
import random
from typing import cast, override
from pywidevine.cdm import Cdm
from pywidevine.device import Device
from pywidevine.pssh import PSSH
import requests

from spotify_dl.api.web.apresolve import get_random_spclient
from spotify_dl.key_provider import KeyProvider
from spotify_dl.auth.internal_auth import SpotifyInternalAuth


class WidevineClient(KeyProvider):
    def __init__(
        self, iauth: SpotifyInternalAuth, widevine_license: Path | str
    ) -> None:
        self.iauth: SpotifyInternalAuth = iauth
        self.device: Device = Device.load(widevine_license)
        self.cdm: Cdm = Cdm.from_device(self.device)

        self.session: bytes = self.cdm.open()

    @override
    def get_audio_key(self, gid: bytes, file_id: bytes) -> bytes | None:
        pssh = PSSH(
            cast(
                str,
                requests.get(
                    f"https://seektables.scdn.co/seektable/{file_id.decode()}.json"
                ).json()["pssh"],
            )
        )

        challenge = self.cdm.get_license_challenge(
            self.session,
            pssh,
            license_type="AUTOMATIC",
            privacy_mode=False,
        )

        # TODO: keep getting 403 error
        license = self.iauth.session.post(
            f"https://{get_random_spclient()[0]}/widevine-license/v1/audio/license",
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en",
            },
            data=challenge,
        )
        license.raise_for_status()
        self.cdm.parse_license(self.session, license.content)

        keys = self.cdm.get_keys(self.session)

        key = random.choice(keys)

        return key.key


if __name__ == "__main__":
    pass
