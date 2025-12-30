import time
from typing import TypeGuard, TypedDict, override

import curl_cffi

from spotify_dl.api.internal.proto.connectivity_pb2 import (
    ConnectivitySdkData,
    NativeDesktopLinuxData,
    PlatformSpecificData,
)
from spotify_dl.api.internal.spotify_client import SpotifyClient
from spotify_dl.auth.auth_provider import AuthProvider
from spotify_dl.auth.web_auth import SpotifyAuthPKCE
from spotify_dl.api.internal.proto.spotify.clienttoken.v0.clienttoken_http_pb2 import (
    REQUEST_CLIENT_DATA_REQUEST,
    RESPONSE_GRANTED_TOKEN_RESPONSE,
    ClientDataRequest,
    ClientTokenRequest,
    ClientTokenResponse,
)
from spotify_dl.utils.session import Session


class ClientTokenSchema(TypedDict):
    token: str
    expires_at: int


class ClientToken(AuthProvider[ClientTokenSchema]):
    def __init__(self, client: SpotifyClient) -> None:
        super().__init__(key="clienttoken")

        self.client: SpotifyClient = client
        self.session: Session = Session(self)

    def _request(self) -> ClientTokenSchema:
        req = ClientTokenRequest(
            request_type=REQUEST_CLIENT_DATA_REQUEST,
            client_data=ClientDataRequest(
                client_version="1.2.78.175",
                client_id=SpotifyAuthPKCE.CLIENT_ID,
                connectivity_sdk_data=ConnectivitySdkData(
                    device_id=self.client.device_id,
                    platform_specific_data=PlatformSpecificData(
                        desktop_linux=NativeDesktopLinuxData(
                            system_name="Linux",
                            system_release="unknown",
                            system_version="0",
                            hardware="x86_64",
                        )
                    ),
                ),
            ),
        )

        resp = curl_cffi.post(
            "https://clienttoken.spotify.com/v1/clienttoken",
            headers={
                "Accept": "application/x-protobuf",
            },
            data=req.SerializeToString(),
            impersonate="chrome",
        )
        resp.raise_for_status()

        res = ClientTokenResponse()
        _ = res.ParseFromString(resp.content)

        if res.response_type != RESPONSE_GRANTED_TOKEN_RESPONSE:
            raise ValueError("failed to get clienttoken")

        return {
            "token": res.granted_token.token,
            "expires_at": int(time.time() + res.granted_token.expires_after_seconds),
        }

    @property
    @override
    def token(self) -> str:
        if not self.is_token_valid():
            self.refresh_token()

        if not self._token:
            raise

        return self._token["token"]

    @override
    def is_token_valid(
        self, token: ClientTokenSchema | None = None
    ) -> TypeGuard[ClientTokenSchema]:
        token = token or self._token
        if not token or "token" not in token:
            return False

        if self.is_token_expired(token):
            return False

        return True

    @override
    def is_token_expired(self, token: ClientTokenSchema | None = None) -> bool:
        if not token:
            return True

        return time.time() > token["expires_at"]

    @override
    def refresh_token(self) -> None:
        self._save(self._request())
