from app.domain.exceptions.auth import AuthorizationError
from app.domain.services.authorization.base import Permission


class AuthorizationService:
    def authorize(self, permission: Permission) -> None:
        if not permission.is_satisfied():
            raise AuthorizationError("Access denied.")
