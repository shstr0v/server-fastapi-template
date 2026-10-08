from dishka import FromDishka
from dishka.integrations.taskiq import inject

from app.application.common.otp.service import OtpService
from app.application.dto.otp import SendOtpDTO


@inject
async def send_otp(data: SendOtpDTO, otp_service: FromDishka[OtpService]) -> None:
    await otp_service.send(data)
