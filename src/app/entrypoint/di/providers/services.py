from dishka import Provider, Scope, provide_all, WithParents

from app.application.services.otp import OtpServiceImpl
from app.application.services.user import UserServiceImpl
from app.application.services.session import SessionServiceImpl


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    provides = provide_all(
        WithParents[OtpServiceImpl],
        WithParents[UserServiceImpl],
        WithParents[SessionServiceImpl],
    )
