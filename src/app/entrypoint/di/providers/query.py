from dishka import Provider, Scope, WithParents, provide_all

from app.application.queries.user import GetMe


class QueryProvider(Provider):
    scope = Scope.REQUEST

    provides = provide_all(
        WithParents[GetMe],
    )
