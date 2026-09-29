from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions import (
    AuthorizationError,
    ConflictError,
    NotFoundError,
    ValidationError,
)


def register_exception_handlers(app):

    @app.exception_handler(NotFoundError)
    async def not_found_handler(
        request: Request,
        exc: NotFoundError,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "detail": str(exc),
            },
        )

    @app.exception_handler(ConflictError)
    async def conflict_handler(
        request: Request,
        exc: ConflictError,
    ):
        return JSONResponse(
            status_code=409,
            content={
                "detail": str(exc),
            },
        )

    @app.exception_handler(ValidationError)
    async def validation_handler(
        request: Request,
        exc: ValidationError,
    ):
        return JSONResponse(
            status_code=400,
            content={
                "detail": str(exc),
            },
        )

    @app.exception_handler(AuthorizationError)
    async def authorization_handler(
        request: Request,
        exc: AuthorizationError,
    ):
        return JSONResponse(
            status_code=403,
            content={
                "detail": str(exc),
            },
        )