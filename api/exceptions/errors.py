class AppError(Exception):
    pass


class NotFoundError(AppError):
    pass


class ConflictError(AppError):
    pass


class ValidationError(AppError):
    pass


class AuthenticationError(AppError):
    pass


class AuthorizationError(AppError):
    pass


class ExternalServiceError(AppError):
    pass
