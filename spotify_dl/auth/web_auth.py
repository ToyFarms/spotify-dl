# pyright: reportIgnoreCommentWithoutRule=false

import base64
import hashlib
import secrets
import logging
import threading
import time
import typing
import webbrowser
import requests
import sys

from flask import Flask, request
from typing import TypeGuard, TypedDict, final, override

from spotify_dl.auth.auth_provider import AuthProvider
from spotify_dl.utils.misc import url_build
from spotify_dl.utils.session import Session


class SpotifyTokenSchema(TypedDict):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str | None
    scope: str
    expires_at: int


logging.getLogger("werkzeug").setLevel(logging.ERROR)

cli = sys.modules["flask.cli"]
cli.show_server_banner = lambda *_: None  # pyright: ignore

app = Flask(__name__)
_callback_code: str | None = None
callback_done = threading.Condition()


@app.route("/login")
def callback():
    global _callback_code

    _ = callback_done.acquire()

    error = request.args.get("error")
    if error:
        return f"Error: {error}", 400

    _callback_code = request.args.get("code")
    callback_done.notify_all()

    callback_done.release()

    return "Spotify authorization successful! You can close this window."


@final
class SpotifyAuthPKCE(AuthProvider[SpotifyTokenSchema]):
    CLIENT_ID: str = "65b708073fc0480ea92a077233ca87bd"
    REDIRECT_URI: str = "http://127.0.0.1:8898/login"

    def __init__(self, scope: str) -> None:
        super().__init__(key="web-auth")

        self.scope: str = scope
        self._verifier: bytes = b""
        self._challenge: bytes = b""
        self.session: Session = Session(self)

    def create_auth_url(self) -> str:
        self._verifier = _code_verifier(64)
        self._challenge = _code_challenge(self._verifier)

        return url_build(
            "https://accounts.spotify.com/authorize",
            client_id=SpotifyAuthPKCE.CLIENT_ID,
            response_type="code",
            redirect_uri=SpotifyAuthPKCE.REDIRECT_URI,
            code_challenge_method="S256",
            code_challenge=self._challenge.decode("utf-8"),
            scope=self.scope,
        )

    def authenticate(self) -> None:
        if self.require_login():
            self._authenticate()
        elif self.is_token_expired(self._token):
            self.refresh_token()

        if not self.is_token_valid(self._token):
            raise ValueError("Token is invalid")

    @property
    @override
    def token(self) -> str:
        self.authenticate()

        if not self._token:
            raise

        return self._token["access_token"]

    @override
    def is_token_valid(
        self, token: SpotifyTokenSchema | None = None
    ) -> TypeGuard[SpotifyTokenSchema]:
        token = token or self._token
        if not token or "access_token" not in token:
            return False

        if time.time() >= token.get("expires_at", 0):
            return False

        return True

    def require_login(self) -> bool:
        return not self._token or "access_token" not in self._token

    @override
    def is_token_expired(self, token: SpotifyTokenSchema | None = None) -> bool:
        token = token or self._token
        if not token:
            return True

        return time.time() >= token.get("expires_at", 0)

    @override
    def refresh_token(self) -> None:
        if not self._token:
            raise ValueError("Expecting some token")

        if "refresh_token" not in self._token:
            raise ValueError("No refresh token available")

        token = self._request_token(
            {
                "client_id": SpotifyAuthPKCE.CLIENT_ID,
                "grant_type": "refresh_token",
                "refresh_token": self._token["refresh_token"],
            }
        )
        self._save(token)

    def _authenticate(self) -> None:
        self._run_server()

        url = self.create_auth_url()
        if not webbrowser.open(url):
            raise Exception(f"Cannot open url: {url}")

        code = self._wait_for_server()

        token = self._request_token(
            {
                "client_id": SpotifyAuthPKCE.CLIENT_ID,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": SpotifyAuthPKCE.REDIRECT_URI,
                "code_verifier": self._verifier,
            }
        )
        self._save(token)

    def _run_server(self) -> None:
        thread = threading.Thread(target=lambda: app.run(port=8898), daemon=True)
        thread.start()

    def _wait_for_server(self) -> str:
        global _callback_code

        _ = callback_done.acquire()

        while not _callback_code:
            _ = callback_done.wait()

        code = _callback_code
        _callback_code = None

        callback_done.release()

        return code

    def _request_token(self, data: dict[str, object]) -> SpotifyTokenSchema:
        res = requests.post(
            "https://accounts.spotify.com/api/token",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        res.raise_for_status()

        return typing.cast(SpotifyTokenSchema, res.json())

    @override
    def _save(self, token: SpotifyTokenSchema | None) -> None:
        token["expires_at"] = int(time.time()) + token["expires_in"]
        refresh_token = self._token.get("refresh_token") if self._token else None
        super()._save(token)

        if self._token and not token.get("refresh_token") and refresh_token:
            self._token["refresh_token"] = refresh_token


def _code_verifier(length: int) -> bytes:
    return base64.urlsafe_b64encode(secrets.token_bytes(length)).rstrip(b"=")


def _code_challenge(verifier: bytes) -> bytes:
    digest = hashlib.sha256(verifier).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=")
