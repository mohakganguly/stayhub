class AppException(Exception):
    """Base exception for application errors."""


class NotFoundError(AppException):
    """Raised when a requested resource does not exist."""


class ConflictError(AppException):
    """Raised when an operation conflicts with existing state."""


class ValidationError(AppException):
    """Raised when business validation fails."""


class AuthorizationError(AppException):
    """Raised when a user is not allowed to perform an action."""