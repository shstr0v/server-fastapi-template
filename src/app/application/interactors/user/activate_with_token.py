from app.adapters.auth.token_processor import TokenProcessor
from app.application.common.interactor import Interactor
from app.application.common.user.service import UserService
from app.application.dto.user import ActivateUserWithTokenCommandDTO, UserActivateDTO, UserDTO


class ActivateUserWithTokenInteractor(Interactor[ActivateUserWithTokenCommandDTO, UserDTO]):
    def __init__(self, token_processor: TokenProcessor, user_service: UserService) -> None:
        self.token_processor = token_processor
        self.user_service = user_service

    async def __call__(self, data: ActivateUserWithTokenCommandDTO) -> UserDTO:
        user_id = self.token_processor.validate_token(data.token)
        return await self.user_service.activate_user(UserActivateDTO(user_id=user_id))
