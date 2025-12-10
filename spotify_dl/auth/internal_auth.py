import time
import typing
import requests

from typing import TypeGuard, TypedDict, override

from spotify_dl.api.internal.totp import create_otp_auth_url
from spotify_dl.auth.auth_provider import AuthProvider
from spotify_dl.auth.spdc import SpDCAuth
from spotify_dl.utils.session import Session


class SpotifyITokenSchema(TypedDict):
    clientId: str
    accessToken: str
    accessTokenExpirationTimestampMs: int
    isAnonymous: bool
    totpValidity: bool
    expires_at: int


# TODO: possibly create 2 version of this, SpotifyInternalAuthWithDc
class SpotifyInternalAuth(AuthProvider[SpotifyITokenSchema]):
    def __init__(self, sp_dc: SpDCAuth | None = None) -> None:
        super().__init__(key="internal-auth-anon" if not sp_dc else "internal-auth")
        self.session: Session = Session(self)
        self.sp_dc: SpDCAuth | None = sp_dc

    def is_linked_with_account(self) -> bool | None:
        if not self._token:
            return

        return not self._token.get("isAnonymous")

    def authenticate(self) -> None:
        if self.require_login() or self.is_token_expired():
            self._authenticate()

        if not self.is_token_valid(self._token):
            raise ValueError("Token is invalid")

    @override
    def refresh_token(self) -> None:
        pass

    @property
    @override
    def token(self) -> str:
        self.authenticate()

        if not self._token:
            raise

        return self._token["accessToken"]

    @override
    def is_token_valid(
        self, token: SpotifyITokenSchema | None = None
    ) -> TypeGuard[SpotifyITokenSchema]:
        token = token or self._token
        if not token or "accessToken" not in token:
            return False

        if time.time() >= token.get("expires_at", 0):
            return False

        return True

    def require_login(self) -> bool:
        return not self._token or "accessToken" not in self._token

    @override
    def is_token_expired(self, token: SpotifyITokenSchema | None = None) -> bool:
        token = token or self._token
        if not token:
            return True

        return time.time() >= token.get("expires_at", 0)

    def _authenticate(self) -> None:
        token = self._request_token()
        self._save(token)

    def _request_token(self) -> SpotifyITokenSchema:
        url = create_otp_auth_url()

        if self.sp_dc:
            res = self.sp_dc.session.get(url)
        else:
            res = requests.get(url)  # anonymous token
        res.raise_for_status()

        return typing.cast(SpotifyITokenSchema, res.json())

    @override
    def _save(self, token: SpotifyITokenSchema | None) -> None:
        if token:
            token["expires_at"] = int(token["accessTokenExpirationTimestampMs"] / 1000)
            super()._save(token)
