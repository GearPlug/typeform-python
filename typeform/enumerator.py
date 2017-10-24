from enum import Enum

class ErrorEnum(Enum):
    Forbidden = 403
    Not_Found = 404
    Payment_Required = 402
    Internal_Server_Error = 500
    Service_Unavailable = 503
    Bad_Request = 400
    Unauthorized = 401