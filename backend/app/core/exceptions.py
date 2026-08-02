from fastapi import status


class AppError(Exception):
    """Base class for all application-raised errors. Caught by the global
    exception handler in app/middlewares/exception_middleware.py and turned
    into a consistent JSON error response."""

    status_code: int = status.HTTP_400_BAD_REQUEST
    error_code: str = "app_error"

    def __init__(self, message: str, status_code: int | None = None, error_code: str | None = None):
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        if error_code is not None:
            self.error_code = error_code
        super().__init__(message)


class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "not_found"


class AlreadyExistsError(AppError):
    status_code = status.HTTP_409_CONFLICT
    error_code = "already_exists"


class InvalidCredentialsError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "invalid_credentials"


class InactiveUserError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "inactive_user"


class PermissionDeniedError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "permission_denied"


class InvalidTokenError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "invalid_token"


class FileTooLargeError(AppError):
    status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    error_code = "file_too_large"


class UnsupportedFileTypeError(AppError):
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    error_code = "unsupported_file_type"


class VirusDetectedError(AppError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    error_code = "virus_detected"


class ScanUnavailableError(AppError):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    error_code = "scan_unavailable"


class StorageNotConfiguredError(AppError):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    error_code = "storage_not_configured"
