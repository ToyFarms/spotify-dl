from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping

from spotify_dl.api.internal.playplay import PlayPlay
from spotify_dl.api.internal.spotify_client import SpotifyClient
from spotify_dl.api.internal.widevine import WidevineClient
from spotify_dl.auth.clienttoken import ClientToken
from spotify_dl.auth.internal_auth import SpotifyInternalAuth
from spotify_dl.auth.login5 import Login5Auth
from spotify_dl.auth.web_auth import SpotifyAuthPKCE
from spotify_dl.downloader import SpotifyDownloadManager


@dataclass
class AppState:
    auth: SpotifyAuthPKCE
    iauth: SpotifyInternalAuth | None = None
    name: str | None = None
    client: SpotifyClient | None = None
    running: bool = True
    last_json_output: Mapping[str, object] | str = field(default_factory=dict)
    dir: Path | None = None
    download_manager: SpotifyDownloadManager = field(
        default_factory=lambda: SpotifyDownloadManager(concurrent_download=2)
    )
    volume: float = 100
    widevine: WidevineClient | None = None
    playplay: PlayPlay | None = None
    login5: Login5Auth | None = None
    clienttoken: ClientToken | None = None

    def ensure_clienttoken(self) -> ClientToken:
        if not self.client:
            self.client = SpotifyClient.random_ap(self.auth)
        if not self.clienttoken:
            self.clienttoken = ClientToken(self.client)

        return self.clienttoken

    def ensure_login5(self) -> Login5Auth:
        if not self.client:
            self.client = SpotifyClient.random_ap(self.auth)
        if not self.clienttoken:
            self.clienttoken = ClientToken(self.client)

        if not self.login5:
            self.login5 = Login5Auth(self.client, self.clienttoken)

        return self.login5


state = AppState(
    auth=SpotifyAuthPKCE("user-read-private streaming"),
)
