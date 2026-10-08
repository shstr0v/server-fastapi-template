from app.application.common.interactor import Interactor
from app.application.common.auth.session import SessionService
from app.application.dto.session import DeleteSessionDTO
from app.adapters.auth.idp import BearerParser
from app.adapters.auth.idp import SessionIdProvider
from app.application.errors.auth import UnauthorizedError


class Logout(Interactor[None, None]):
    def __init__(
        self,
        bearer_parser: BearerParser,
        idp: SessionIdProvider,
        session_service: SessionService,
    ) -> None:
        self.bearer_parser = bearer_parser
        self.idp = idp
        self.session_service = session_service

    async def __call__(self) -> None:
        try:
            user_id = await self.idp.get_current_id()
            current_sid = self.idp.get_current_sid()
            await self.session_service.terminate(DeleteSessionDTO(user_id=user_id, session_id=current_sid))
        except UnauthorizedError:
            return
