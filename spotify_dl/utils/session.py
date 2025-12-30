# pyright: reportAny=false, reportExplicitAny=false

from typing import Any, Callable, override
import curl_cffi

from spotify_dl.auth.auth_provider import AuthProvider


class Session(curl_cffi.Session):
    def __init__(
        self,
        auth: AuthProvider[Any],
        handler: Callable[["Session"], Any] | None = None,
    ) -> None:
        super().__init__(impersonate="chrome")

        self._auth: AuthProvider[Any] = auth
        self._handler: Callable[["Session"], Any] | None = handler

    @override
    def request(self, *args: Any, **kwargs: Any) -> curl_cffi.Response:
        if self._handler:
            self._handler(self)
        else:
            self.headers.update({"Authorization": f"Bearer {self._auth.token}"})
        return super().request(*args, **kwargs)  # pyright: ignore[reportUnknownMemberType]
