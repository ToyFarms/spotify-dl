# pyright: reportAny=false, reportExplicitAny=false

from typing import Any, override
import requests

from spotify_dl.auth.protocol import AuthProtocol


class Session(requests.Session):
    def __init__(self, auth: AuthProtocol) -> None:
        super().__init__()

        self._auth: AuthProtocol = auth

    @override
    def request(self, *args: Any, **kwargs: Any) -> requests.Response:
        self.headers.update({"Authorization": f"Bearer {self._auth.token}"})
        return super().request(*args, **kwargs)
