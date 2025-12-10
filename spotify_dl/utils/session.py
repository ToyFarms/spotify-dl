# pyright: reportAny=false, reportExplicitAny=false

from typing import Any, Callable, override
import requests

from spotify_dl.auth.auth_provider import AuthProvider


class Session(requests.Session):
    def __init__(
        self,
        auth: AuthProvider[Any],
        handler: Callable[["Session"], Any] | None = None,
    ) -> None:
        super().__init__()

        self._auth: AuthProvider[Any] = auth
        self._handler: Callable[["Session"], Any] | None = handler

    @override
    def request(self, *args: Any, **kwargs: Any) -> requests.Response:
        if self._handler:
            self._handler(self)
        else:
            self.headers.update({"Authorization": f"Bearer {self._auth.token}"})
        return super().request(*args, **kwargs)
