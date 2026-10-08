from app.application.common.interactor import Interactor
from app.application.dto.user import UpdateUserDTO, UserDTO
from app.application.errors.user import UserNotFoundError
from app.application.common.user.repository import UserRepository
from app.domain.entities.user.value_objects import UserId, UserFullname, AvatarUrl, Username
from app.application.common.user.dao import UserDAO
from app.application.common.uow import UoW
from app.adapters.auth.idp import SessionIdProvider


class UpdateUser(Interactor[UpdateUserDTO, UserDTO]):
    def __init__(
        self, 
        repository: UserRepository, 
        dao: UserDAO, 
        uow: UoW, 
        idp: SessionIdProvider,
    ) -> None:
        self.repository = repository
        self.dao = dao
        self.uow = uow
        self.idp = idp

    async def __call__(self, data: UpdateUserDTO) -> UserDTO:
        user_id = await self.idp.get_current_id()
        user = await self.repository.get_user(UserId(user_id.raw()))
        if user is None:
            raise UserNotFoundError("User not found.")

        user.update(
            email=user.email,
            fullname=UserFullname(data.first_name, data.last_name),
            age=user.age,
            username=Username(data.username),
            gender=data.gender if data.gender else user.gender,
            avatar_url=AvatarUrl(data.avatar_url) if data.avatar_url else None,
        )
        await self.repository.update(user)
        await self.uow.commit()
        return await self.dao.get_by_id(user_id=user.id.value)
