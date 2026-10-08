from dishka import Provider, Scope, WithParents, provide_all

from app.adapters.data.repository import (
    OtpRepositoryImpl,
    UserRepositoryImpl,
)


class RepositoryProvider(Provider):
    scope = Scope.REQUEST

    provides = provide_all(
        WithParents[OtpRepositoryImpl],
        WithParents[UserRepositoryImpl],
    )
