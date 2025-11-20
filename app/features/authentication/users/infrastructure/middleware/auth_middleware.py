from typing import Callable, Iterable, Tuple

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.features.authentication.users.application.internal.outbound_services.token_service.token_service import (
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
        if request.method == "OPTIONS":
            return await call_next(request)

        path = request.url.path
        # Debugging output: show path and configured public paths/prefixes
        try:
            print(
                f"AuthMiddleware: incoming path={path}, public_paths={self.public_paths}, public_prefixes={self.public_prefixes}"
            )
        except Exception:
            pass
        if self._is_public(path):
            request.state.user_id = None
            request.state.jwt_payload = None
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            print(f"AuthMiddleware: missing/invalid Authorization header for path {path}")
            return JSONResponse({"detail": "Unauthorized"}, status_code=401)

        token = auth_header.split(" ", 1)[1]
        payload = self.token_service.verify_token(token)
        if not payload:
            print(f"AuthMiddleware: token invalid for path {path}")
            return JSONResponse({"detail": "Invalid token"}, status_code=401)

        request.state.jwt_payload = payload
        request.state.user_id = payload.get("user_id")
        request.state.email = payload.get("sub")

        return await call_next(request)
