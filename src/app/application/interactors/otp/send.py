from app.application.common.interactor import Interactor
from app.application.common.uow import UoW
from app.application.common.otp.service import OtpService
from app.application.common.user.dao import UserDAO
from app.application.dto.otp import SendOtpDTO, OtpDTO


class SendOtp(Interactor[SendOtpDTO, OtpDTO]):
    def __init__(
        self,
        uow: UoW,
        otp_service: OtpService,
        user_query: UserDAO,
    ) -> None:
        self.uow = uow
        self.otp_service = otp_service
        self.user_query = user_query

    async def __call__(self, data: SendOtpDTO) -> OtpDTO:
        otp = await self.otp_service.send(data)
        await self.uow.commit()

        return otp
