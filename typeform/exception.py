class BaseError(Exception):
    pass


class CredentialRequired(BaseError):
    pass


class UnexpectedError(BaseError):
    pass


class Forbidden(BaseError):
    pass


class NotFound(BaseError):
    pass


class PaymentRequired(BaseError):
    pass


class InternalServerError(BaseError):
    pass


class ServiceUnavailable(BaseError):
    pass


class BadRequest(BaseError):
    pass


class Unauthorized(BaseError):
    pass


class TokenRequired(BaseError):
    pass
