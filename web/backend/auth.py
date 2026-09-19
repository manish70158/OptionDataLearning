"""HTTP Basic Auth gate for the deployed app.

Credentials come from the ``WEB_AUTH_USER`` / ``WEB_AUTH_PASS`` env vars.
When either is unset (typical local dev), auth is disabled and every
request is allowed through — matching the previous no-auth behaviour.
"""
from __future__ import annotations

import os
import secrets
from typing import Callable

from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

# Anything under these prefixes is served without auth so a user can hit
# ``/api/auth/upstox/callback`` from Upstox's OAuth redirect and see the
# health endpoint from Render's uptime probe without credentials.
_OPEN_PATHS = ("/api/health", "/api/auth/upstox/")


class BasicAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.user = os.environ.get("WEB_AUTH_USER") or ""
        self.password = os.environ.get("WEB_AUTH_PASS") or ""
        self.enabled = bool(self.user and self.password)

    async def dispatch(self, request: Request, call_next: Callable):
        if not self.enabled or self._is_open(request.url.path):
            return await call_next(request)

        if self._authorized(request):
            return await call_next(request)

        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": 'Basic realm="Options Backtester"'},
        )

    def _is_open(self, path: str) -> bool:
        return any(path == p or path.startswith(p) for p in _OPEN_PATHS)

    def _authorized(self, request: Request) -> bool:
        header = request.headers.get("authorization", "")
        if not header.startswith("Basic "):
            return False
        import base64
        try:
            decoded = base64.b64decode(header[6:]).decode("utf-8", errors="replace")
            user, _, password = decoded.partition(":")
        except (ValueError, UnicodeDecodeError):
            return False
        # Constant-time comparison avoids timing side-channel leaks.
        return secrets.compare_digest(user, self.user) and secrets.compare_digest(password, self.password)
