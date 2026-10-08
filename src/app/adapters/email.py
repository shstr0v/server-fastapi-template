from email.message import EmailMessage

import aiosmtplib

from app.adapters.config import EmailConfig
from app.application.common.email_sender import EmailSender
from app.application.dto.email import EmailMessageDTO
from app.application.errors.email import EmailSendingError


class EmailSenderImpl(EmailSender):
    def __init__(self, config: EmailConfig) -> None:
        self.config = config

    async def send(self, data: EmailMessageDTO) -> None:
        message = EmailMessage()
        message["From"] = self.config.from_email
        message["To"] = data.to
        message["Subject"] = data.subject
        message.set_content(data.body)
        if data.html:
            message.add_alternative(data.html, subtype="html")

        try:
            await aiosmtplib.send(
                message,
                hostname=self.config.hostname,
                port=int(self.config.port),
                username=self.config.username or None,
                password=self.config.password or None,
                start_tls=True,
            )
        except aiosmtplib.SMTPException as exc:
            raise EmailSendingError("Unable to send email.") from exc
