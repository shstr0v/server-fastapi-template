from dataclasses import dataclass

from app.adapters.auth.idp import SessionIdProvider
from app.adapters.config import AwsConfig
from app.application.common.file_manager import AwsFileManager
from app.application.common.interactor import Interactor
from app.application.dto.aws import PresignedDownloadDTO, PresignedUploadDTO
from app.application.interactors.uploads.keys import new_object_key, owned_object_key


@dataclass(frozen=True)
class CreatePresignedUploadDTO:
    file_name: str
    content_type: str
    folder: str = "uploads"


@dataclass(frozen=True)
class PresignedUploadResultDTO:
    file_url: str
    key: str
    upload_url: str


@dataclass(frozen=True)
class CreatePresignedDownloadDTO:
    key: str


@dataclass(frozen=True)
class PresignedDownloadResultDTO:
    key: str
    download_url: str


class CreatePresignedUpload(Interactor[CreatePresignedUploadDTO, PresignedUploadResultDTO]):
    def __init__(
        self,
        file_manager: AwsFileManager,
        config: AwsConfig,
        idp: SessionIdProvider,
    ) -> None:
        self.file_manager = file_manager
        self.config = config
        self.idp = idp

    async def __call__(self, data: CreatePresignedUploadDTO) -> PresignedUploadResultDTO:
        user_id = await self.idp.get_current_id()
        key = new_object_key(user_id.value, data.file_name, data.folder)
        presigned = await self.file_manager.create_upload_url(
            PresignedUploadDTO(key=key, content_type=data.content_type)
        )
        return PresignedUploadResultDTO(
            file_url=self.config.object_url(presigned.key),
            key=presigned.key,
            upload_url=presigned.url,
        )


class CreatePresignedDownload(Interactor[CreatePresignedDownloadDTO, PresignedDownloadResultDTO]):
    def __init__(
        self,
        file_manager: AwsFileManager,
        idp: SessionIdProvider,
    ) -> None:
        self.file_manager = file_manager
        self.idp = idp

    async def __call__(self, data: CreatePresignedDownloadDTO) -> PresignedDownloadResultDTO:
        user_id = await self.idp.get_current_id()
        key = owned_object_key(user_id.value, data.key)
        presigned = await self.file_manager.create_download_url(PresignedDownloadDTO(key=key))
        return PresignedDownloadResultDTO(key=presigned.key, download_url=presigned.url)
