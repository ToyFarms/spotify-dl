# pyright: reportUnknownMemberType=false, reportUnknownLambdaType=false

from typing import TypeGuard, TypedDict, final, override

from spotify_dl.auth.auth_provider import AuthProvider
from spotify_dl.utils.session import Session


class SpDCSchema(TypedDict):
    spdc: str


@final
class SpDCAuth(AuthProvider[SpDCSchema]):
    def __init__(self) -> None:
        super().__init__(key="spdc")
        self._token: SpDCSchema | None = self._load()
        self.session: Session = Session(
            self,
            handler=lambda s: s.cookies.update({"sp_dc": self.token}),
        )

    @override
    def is_token_expired(self, token: SpDCSchema | None = None) -> bool:
        return False

    @override
    def is_token_valid(self, token: SpDCSchema | None = None) -> TypeGuard[SpDCSchema]:
        token = token or self._token
        return token is not None

    @override
    def refresh_token(self) -> None:
        pass

    @property
    @override
    def token(self) -> str:
        if not self.is_token_valid():
            spdc = input("your sp_dc (get from browser) > ")
            if not spdc:
                raise ValueError

            self._token = {"spdc": spdc}
            self._save(self._token)

        if not self._token:
            raise

        return self._token["spdc"]
