class AwsError(Exception):
    ...


class PresignedUrlError(AwsError):
    ...


class InvalidObjectKeyError(AwsError):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
