from rest_framework.exceptions import APIException

from typing import Optional, Union

from django.utils.functional import Promise
from rest_framework import status
from rest_framework.exceptions import APIException
from pydantic import BaseModel

class ApiErrorData(BaseModel):
    detail: Union[str, Promise]
    code: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

class ExtendedAPIException(APIException):
    def __init__(self, detail=None, code=None):
        if isinstance(detail, ApiErrorData):
            super().__init__(detail=detail.detail, code=detail.code)
            return
        super().__init__(detail, code)

class AuthenticationException(ExtendedAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
class BadRequestException(ExtendedAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
class NotFoundException(ExtendedAPIException):
    status_code = status.HTTP_404_NOT_FOUND
class UnauthorizedException(ExtendedAPIException):
    status_code = status.HTTP_403_FORBIDDEN
class InternalServerException(ExtendedAPIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

class IntegrityErrorException(ExtendedAPIException):
    status_code = status.HTTP_409_CONFLICT  