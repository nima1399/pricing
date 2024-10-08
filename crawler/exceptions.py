from rest_framework.exceptions import APIException


class ServerError(APIException):
    status_code = 500
    default_detail = "A server error occurred."
    default_code = "server_error"


class ClientError(APIException):
    status_code = 400
    default_detail = "A client error occurred."
    default_code = "client_error"
