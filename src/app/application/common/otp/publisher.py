from abc import abstractmethod
from typing import Protocol

from app.application.dto.otp import SendOtpDTO


class OtpPublisher(Protocol):
    @abstractmethod
    async def publish(self, data: SendOtpDTO) -> None:
        raise NotImplementedError
