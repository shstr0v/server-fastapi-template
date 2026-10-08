from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.application.common.error import ApplicationError
from app.application.errors.auth import UnauthorizedError
from app.application.errors.aws import InvalidObjectKeyError, PresignedUrlError
from app.application.errors.user import UserNotFoundError
from app.presentation.http.routers.auth import router as auth_router
from app.presentation.http.routers.uploads import router as uploads_router
from app.presentation.http.routers.users import router as users_router


def include_routers(app: FastAPI) -> None:
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(uploads_router)


def include_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UnauthorizedError)
    async def unauthorized_handler(request: Request, exc: UnauthorizedError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": getattr(exc, "message", "Unauthorized")},
        )

    @app.exception_handler(UserNotFoundError)
    async def user_not_found_handler(request: Request, exc: UserNotFoundError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc) or "User not found"},
        )

    @app.exception_handler(InvalidObjectKeyError)
    async def invalid_object_key_handler(request: Request, exc: InvalidObjectKeyError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.message},
        )

    @app.exception_handler(PresignedUrlError)
    async def presigned_url_handler(request: Request, exc: PresignedUrlError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content={"detail": str(exc) or "Unable to create a presigned URL."},
        )

    @app.exception_handler(ApplicationError)
    async def application_error_handler(request: Request, exc: ApplicationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": getattr(exc, "message", str(exc) or "Application error")},
        )
