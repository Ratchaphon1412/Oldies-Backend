from rest_framework import status
from rest_framework.exceptions import APIException


class BadRequestBody(APIException):
        status_code = status.HTTP_400_BAD_REQUEST
        default_detail = "The request body is not valid or Incorrect"
        default_code = "bad_request_body"

class NotAcceptableCreateAccount(APIException):
        status_code = status.HTTP_406_NOT_ACCEPTABLE
        default_detail = "The request body is not valid or Incorrect or Email already exists"
        default_code = "not_acceptable_create_account"

class EmailNotVerified(APIException):
        status_code = status.HTTP_406_NOT_ACCEPTABLE
        default_detail = "Email is not verified"
        default_code = "email_not_verified"

class VerifyEmailError(APIException):
        status_code = status.HTTP_406_NOT_ACCEPTABLE
        default_detail = "Email is not verified because can't decode uid"
        default_code = "email_not_verified"

class EmailErrorSend(APIException):
        status_code = status.HTTP_406_NOT_ACCEPTABLE
        default_detail = "Email is not verified because can't send email"
        default_code = "email_not_verified"