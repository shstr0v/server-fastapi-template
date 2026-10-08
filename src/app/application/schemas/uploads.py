from pydantic import BaseModel, Field


class CreatePresignedUploadRequest(BaseModel):
    file_name: str = Field(min_length=1, max_length=255)
    content_type: str = Field(min_length=1, max_length=255)
    folder: str = Field(default="uploads", min_length=1, max_length=64)


class PresignedUploadResponse(BaseModel):
    file_url: str
    key: str
    upload_url: str


class CreatePresignedDownloadRequest(BaseModel):
    key: str = Field(min_length=1, max_length=1024)


class PresignedDownloadResponse(BaseModel):
    key: str
    download_url: str
