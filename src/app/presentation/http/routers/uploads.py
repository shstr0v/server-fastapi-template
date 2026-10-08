from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter

from app.application.interactors.uploads.presign import (
    CreatePresignedDownload,
    CreatePresignedDownloadDTO,
    CreatePresignedUpload,
    CreatePresignedUploadDTO,
)
from app.application.schemas.uploads import (
    CreatePresignedDownloadRequest,
    CreatePresignedUploadRequest,
    PresignedDownloadResponse,
    PresignedUploadResponse,
)

router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("/presigned-url", response_model=PresignedUploadResponse)
@router.post("/presigned", response_model=PresignedUploadResponse)
@inject
async def create_presigned_upload_url(
    data: CreatePresignedUploadRequest,
    interactor: FromDishka[CreatePresignedUpload],
) -> PresignedUploadResponse:
    result = await interactor(
        CreatePresignedUploadDTO(
            file_name=data.file_name,
            content_type=data.content_type,
            folder=data.folder,
        )
    )
    return PresignedUploadResponse(
        file_url=result.file_url,
        key=result.key,
        upload_url=result.upload_url,
    )


@router.post("/presigned-download", response_model=PresignedDownloadResponse)
@inject
async def create_presigned_download_url(
    data: CreatePresignedDownloadRequest,
    interactor: FromDishka[CreatePresignedDownload],
) -> PresignedDownloadResponse:
    result = await interactor(CreatePresignedDownloadDTO(key=data.key))
    return PresignedDownloadResponse(key=result.key, download_url=result.download_url)
