# pyright: reportExplicitAny=false, reportAny=false

from abc import ABC, abstractmethod
from collections.abc import Mapping
import json
import os
from pathlib import Path
import tempfile
from typing import TypeGuard, cast


class AuthProvider[T: Mapping[str, object]](ABC):
    TOKEN_DIR: Path = Path(".sptoken")

    def __init__(self, key: str) -> None:
        self._key: str = key
        self._token: T | None = self._load()

    @property
    @abstractmethod
    def token(self) -> str:
        pass

    @abstractmethod
    def is_token_valid(self, token: T | None = None) -> TypeGuard[T]:
        pass

    @abstractmethod
    def refresh_token(self) -> None:
        pass

    @abstractmethod
    def is_token_expired(self, token: T | None = None) -> bool:
        pass

    def _save(self, token: T | None) -> None:
        self._token = token
        AuthProvider.TOKEN_DIR.mkdir(exist_ok=True)

        token_path = AuthProvider.TOKEN_DIR / f"{self._key}.json"

        if token is None:
            try:
                token_path.unlink()
            except FileNotFoundError:
                pass
            return

        fd, tmp = tempfile.mkstemp(
            prefix=f".{self._key}.", dir=str(AuthProvider.TOKEN_DIR)
        )
        tmp_path = Path(tmp)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(dict(token), f, indent=4, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())

            os.replace(str(tmp_path), str(token_path))
        finally:
            if tmp_path.exists():
                try:
                    tmp_path.unlink()
                except Exception:
                    pass

    def _load(self) -> T | None:
        token_path = AuthProvider.TOKEN_DIR / f"{self._key}.json"
        if not token_path.exists():
            return None
        try:
            with token_path.open("r", encoding="utf-8") as f:
                # note: keep the return type as T | None; caller may cast
                return cast(T, json.load(f))
        except Exception:
            # corrupted or unreadable file -> treat as missing
            return None
