from dishka import Provider, Scope, WithParents, provide_all

from app.adapters.data.dao import UserDAOImpl


class DAOProvider(Provider):
    scope = Scope.REQUEST

    provides = provide_all(
        WithParents[UserDAOImpl],
    )
