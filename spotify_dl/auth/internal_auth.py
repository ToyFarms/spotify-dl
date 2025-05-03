import json
import time
import typing
import requests

from typing import TypeGuard, TypedDict

from spotify_dl.api.internal.totp import create_otp_auth_url
from spotify_dl.auth.web_auth import SpotifyAuthPKCE
from spotify_dl.utils.session import Session


class SpotifyITokenSchema(TypedDict):
    clientId: str
    accessToken: str
    accessTokenExpirationTimestampMs: int
    isAnonymous: bool
    totpValidity: bool
    expires_at: int


class SpotifyInternalAuth:
    def __init__(
        self, web_auth: SpotifyAuthPKCE, cache_file: str = ".ispotify_token.json"
    ) -> None:
        self.web_auth: SpotifyAuthPKCE = web_auth
        self.cache_file: str = cache_file
        self._token: SpotifyITokenSchema | None = self._load_token(self.cache_file)

        self.session: Session = Session(self)

    def authenticate(self) -> None:
        if self.require_login() or self.token_expired():
            self._authenticate()

        if not self.is_token_valid(self._token):
            raise ValueError("Token is invalid")

    @property
    def token(self) -> str:
        self.authenticate()

        if not self._token:
            raise

        return self._token["accessToken"]

    def is_token_valid(
        self, token: SpotifyITokenSchema | None
    ) -> TypeGuard[SpotifyITokenSchema]:
        if not token or "accessToken" not in token:
            return False

        if time.time() >= token.get("expires_at", 0):
            return False

        return True

    def require_login(self) -> bool:
        return not self._token or "accessToken" not in self._token

    def token_expired(self) -> bool:
        if not self._token:
            return True

        return time.time() >= self._token.get("expires_at", 0)

    def _authenticate(self) -> None:
        token = self._request_token()
        self._save_token(self.cache_file, token)

    def _request_token(self) -> SpotifyITokenSchema:
        url = create_otp_auth_url()

        res = requests.get(url)
        res.raise_for_status()

        return typing.cast(SpotifyITokenSchema, res.json())

    def _save_token(self, path: str, token: SpotifyITokenSchema) -> None:
        token["expires_at"] = int(token["accessTokenExpirationTimestampMs"] / 1000)

        self._token = token

        with open(path, "w") as f:
            json.dump(token, f)

    def _load_token(self, path: str) -> SpotifyITokenSchema | None:
        try:
            with open(path, "r") as f:
                return typing.cast(SpotifyITokenSchema, json.load(f))
        except:
            return None
