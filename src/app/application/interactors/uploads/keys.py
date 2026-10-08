import re
from uuid import UUID, uuid4

from app.application.errors.aws import InvalidObjectKeyError

_SEGMENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
_EXTENSION = re.compile(r"^[A-Za-z0-9]{1,10}$")


def new_object_key(user_id: UUID, file_name: str, folder: str) -> str:
    cleaned_folder = folder.strip("/")
    if not _SEGMENT.fullmatch(cleaned_folder):
        raise InvalidObjectKeyError("Folder must be a single safe path segment.")

    if "/" in file_name or "\\" in file_name or file_name.startswith(".") or "." not in file_name:
        raise InvalidObjectKeyError("File name must include a safe extension.")

    extension = file_name.rsplit(".", 1)[-1]
    if not _EXTENSION.fullmatch(extension):
        raise InvalidObjectKeyError("File extension is not allowed.")

    return f"{cleaned_folder}/{user_id}/{uuid4()}.{extension}"


def owned_object_key(user_id: UUID, key: str) -> str:
    parts = key.strip().lstrip("/").split("/")
    if not parts or any(part in {"", ".", ".."} for part in parts):
        raise InvalidObjectKeyError("Object key is invalid.")
    if str(user_id) not in parts:
        raise InvalidObjectKeyError("Object key is outside the current user's uploads.")
    return "/".join(parts)
