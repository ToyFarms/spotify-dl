# pyright: reportAny=false, reportExplicitAny=false

from typing import Any, override
import requests

from spotify_dl.auth.auth_provider import AuthProvider


class Session(requests.Session):
    def __init__(self, auth: AuthProvider[Any]) -> None:
        super().__init__()

        self._auth: AuthProvider[Any] = auth

    @override
    def request(self, *args: Any, **kwargs: Any) -> requests.Response:
        self.headers.update({"Authorization": f"Bearer {self._auth.token}"})
        return super().request(*args, **kwargs)
