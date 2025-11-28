import base64
import time
from typing import TypeGuard, TypedDict, final, override
import requests
from spotify_dl.api.internal.proto.spotify.login5.v3.client_info_pb2 import ClientInfo
from spotify_dl.api.internal.proto.spotify.login5.v3.credentials.credentials_pb2 import (
    StoredCredential,
)
from spotify_dl.api.internal.spotify_client import SpotifyClient
from spotify_dl.auth.auth_provider import AuthProvider
from spotify_dl.api.internal.proto.spotify.login5.v3.login5_pb2 import (
    ChallengeSolution,
    LoginRequest,
    LoginResponse,
)
from spotify_dl.auth.clienttoken import ClientToken
from spotify_dl.auth.web_auth import SpotifyAuthPKCE
from spotify_dl.utils.hashcash import solve_hash_cash
from spotify_dl.utils.session import Session


class Login5TokenSchema(TypedDict):
    access_token: str
    expires_at: int


@final
class Login5Auth(AuthProvider[Login5TokenSchema]):
    def __init__(self, client: SpotifyClient, clienttoken: ClientToken) -> None:
        super().__init__(key="login5")

        self.client = client
        self.clienttoken = clienttoken
        self.session = Session(self)

    def _request(self) -> Login5TokenSchema:
        login5_req = LoginRequest(
            client_info=ClientInfo(
                client_id=SpotifyAuthPKCE.CLIENT_ID, device_id=self.client.device_id
            ),
            stored_credential=StoredCredential(
                username=self.client.reusable["username"],
                data=base64.b64decode(self.client.reusable["credentials"]),
            ),
        )

        def req(_req: LoginRequest) -> bytes:
            res = requests.post(
                "https://login5.spotify.com/v3/login",
                data=_req.SerializeToString(),
                headers={
                    "Content-Type": "application/x-protobuf",
                    "Accept": "application/x-protobuf",
                    "Client-Token": self.clienttoken.token
                },
            )
            res.raise_for_status()

            return res.content

        login5_res = LoginResponse()
        _ = login5_res.ParseFromString(req(login5_req))

        if not login5_res.ok:
            raise RuntimeError(f"login5 failed: {login5_res.error}")

        if login5_res.challenges:
            ctx = login5_res.login_context
            for challenge in login5_res.challenges.challenges:
                solution = solve_hash_cash(ctx, challenge.hashcash)
                login5_req.challenge_solutions.solutions.append(
                    value=ChallengeSolution(hashcash=solution)
                )

            _ = login5_res.ParseFromString(req(login5_req))

            if not login5_res.ok:
                raise RuntimeError(f"login5 failed: {login5_res.error}")

        return {
            "access_token": login5_res.ok.access_token,
            "expires_at": int(time.time() + login5_res.ok.access_token_expires_in),
        }

    @override
    def is_token_expired(self, token: Login5TokenSchema | None = None) -> bool:
        token = token or self._token
        if not token:
            return True

        return time.time() >= token.get("expires_at", 0)

    @override
    def is_token_valid(
        self, token: Login5TokenSchema | None = None
    ) -> TypeGuard[Login5TokenSchema]:
        token = token or self._token
        if not token or "access_token" not in token:
            return False

        if self.is_token_expired(token):
            return False

        return False

    @override
    def refresh_token(self) -> None:
        self._save(self._request())

    @property
    @override
    def token(self) -> str:
        if not self.is_token_valid(self._token):
            self.refresh_token()

        if not self._token:
            raise

        return self._token["access_token"]
