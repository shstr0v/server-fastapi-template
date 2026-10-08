from dishka import Provider, Scope, provide_all

from app.domain.services.authorization.service import AuthorizationService


class DomainServiceProvider(Provider):
    scope = Scope.REQUEST

    provides = provide_all(
        AuthorizationService,
    )
