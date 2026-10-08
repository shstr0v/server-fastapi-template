from app.application.common.interactor import Interactor
from app.application.dto.auth import PhoneLoginDTO, PhoneLoginResponseDTO
from app.application.dto.otp import SendOtpDTO
from app.application.common.otp.service import OtpService
from app.application.common.user.service import UserService
from app.application.dto.user import CreateUserDTO
from app.application.common.user.dao import UserDAO
from app.application.common.uow import UoW


class PhoneLogin(Interactor[PhoneLoginDTO, PhoneLoginResponseDTO]):
    def __init__(
        self,
        user_service: UserService,
        otp_service: OtpService,
        dao: UserDAO,
        uow: UoW,
    ) -> None:
        self.otp_service = otp_service
        self.user_service = user_service
        self.dao = dao
        self.uow = uow
    
    async def __call__(self, data: PhoneLoginDTO) -> PhoneLoginResponseDTO:
        user = await self.dao.get_by_phone(data.phone, is_active=True)
        if user is None:
            user = await self.user_service.create_user(CreateUserDTO(phone=data.phone)) 
        await self.otp_service.send(
            SendOtpDTO(
                user_id=user.id,
                phone=data.phone,
            )
        )
        user = await self.dao.get_by_id(user_id=user.id)
        await self.uow.commit()

        return PhoneLoginResponseDTO(
            user=user,
        )
