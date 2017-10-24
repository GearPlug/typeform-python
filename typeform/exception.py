class BaseError(Exception):
    pass

class CredentialRequired(BaseError):
    pass

class UnexpectedError(BaseError):
    pass

class Forbidden (BaseError):
    pass

class Not_Found (BaseError):
    pass

class Payment_Required (BaseError):
    pass

class Internal_Server_Error (BaseError):
    pass

class Service_Unavailable (BaseError):
    pass

class Bad_Request (BaseError):
    pass

class Unauthorized (BaseError):
    pass

class TokenRequired(BaseError):
    pass