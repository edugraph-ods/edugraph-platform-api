from typing import Callable, Iterable, Tuple

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.features.authentication.application.internal.outbound_services.token_service.token_service import (
    TokenService,
)


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        token_service: TokenService,
        public_paths: Iterable[str] | None = None,
        public_prefixes: Tuple[str, ...] | None = None,
    ):
        super().__init__(app)
        self.token_service = token_service
        # exact-match or startswith paths considered public
        self.public_paths = set(public_paths or [])
        self.public_prefixes = public_prefixes or (
            "/docs",
            "/openapi.json",
            "/redoc",
            "/favicon.ico",
        )

    def _is_public(self, path: str) -> bool:
        if path in self.public_paths:
            return True
        return any(path.startswith(prefix) for prefix in self.public_prefixes)

    async def dispatch(self, request: Request, call_next: Callable):
        path = request.url.path
        if self._is_public(path):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse({"detail": "Unauthorized"}, status_code=401)

        token = auth_header.split(" ", 1)[1]
        payload = self.token_service.verify_token(token)
        if not payload:
            return JSONResponse({"detail": "Invalid token"}, status_code=401)

        # Make JWT payload available to downstream handlers
        request.state.jwt_payload = payload
        return await call_next(request)
