from app.application.common.otp.service import OtpService
from app.application.common.sms_client import SmsClient
from app.application.common.sms_client import PhoneNumber
from app.application.dto.otp import SendOtpDTO, OtpDTO, CheckOtpDTO
from app.domain.entities.auth.entities import OneTimePasscode
from app.domain.entities.auth.value_objects import Passcode
from app.domain.entities.user.value_objects import UserId, PhoneNumber as UserPhoneNumber
from app.application.common.otp.repository import OtpRepository
from app.application.errors.otp import OtpError
from app.domain.exceptions.auth import PasscodeMismatchError
from app.application.common.user.dao import UserDAO


class OtpServiceImpl(OtpService):
    def __init__(
        self,
        sms_client: SmsClient,
        otp_repository: OtpRepository,
        user_dao: UserDAO,
    ) -> None:
        self.sms_client = sms_client
        self.user_dao = user_dao
        self.otp_repository = otp_repository

    async def send(self, data: SendOtpDTO) -> OtpDTO:
        passcode = OneTimePasscode.create(
            phone=UserPhoneNumber.create(data.phone),
            code=Passcode.generate_code(),
            user_id=UserId(data.user_id),
        )
        await self.sms_client.send_otp(
            to=PhoneNumber(data.phone),
            code=passcode.code.value,
        )
        await self.otp_repository.create(passcode)

        return OtpDTO(
            id=passcode.id.value,
            user_id=passcode.user_id.value,
            code=passcode.code.value,
            phone=passcode.phone.value,
        )

    async def check(self, data: CheckOtpDTO) -> None:
        otp = await self.otp_repository.load_by_user_id(UserId(data.user_id))
        if otp is None:
            raise OtpError("Passcode not found")
        if otp.code.value != data.code:
            raise PasscodeMismatchError()
