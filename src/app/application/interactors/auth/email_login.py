from app.application.common.interactor import Interactor
from app.application.common.user.repository import UserRepository
from app.application.dto.auth import EmailLoginDTO, EmailLoginResponseDTO
from app.application.dto.user import UserDTO
from app.domain.entities.user.value_objects import EmailAddress
from app.application.common.auth.hasher import Hasher
from app.application.errors.auth import (
    InvalidPasswordError,
)
from app.application.common.auth.session import SessionService
from app.application.dto.session import CreateSessionDTO


class EmailLogin(Interactor[EmailLoginDTO, EmailLoginResponseDTO]):
    def __init__(
        self,
        repository: UserRepository,
        hasher: Hasher,
        session_service: SessionService,
    ) -> None:
        self.repository = repository
        self.hasher = hasher
        self.session_service = session_service

    async def __call__(self, data: EmailLoginDTO) -> EmailLoginResponseDTO:
        user = await self.repository.get_user_by_email(EmailAddress(data.email))
        is_password_valid = self.hasher.compare(
            data.raw_password, user.hashed_password.raw()
        )
        if not is_password_valid:
            raise InvalidPasswordError("Password mismatch.")

        user = UserDTO(
            id=user.id.raw(),
            email=user.email.raw() if user.email else None,
            phone=user.phone.raw() if user.phone else None,
            created_at=user.created_at.raw(),
            status=user.status,
        )
        session = await self.session_service.create(CreateSessionDTO(user_id=user.id, user_agent=data.user_agent))

        return EmailLoginResponseDTO(
            user=user,
            sid=session.session,
        )
