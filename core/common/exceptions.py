from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.exceptions import APIException
from django.http import JsonResponse
import logging

logger = logging.getLogger('surgery')


class SurgeryException(APIException):
    def __init__(self, code, message, status_code=status.HTTP_400_BAD_REQUEST):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(detail=message)


class AuthenticationFailedException(SurgeryException):
    def __init__(self, message="認證失敗"):
        super().__init__("401", message, status.HTTP_401_UNAUTHORIZED)


class PermissionDeniedException(SurgeryException):
    def __init__(self, message="權限不足"):
        super().__init__("403", message, status.HTTP_403_FORBIDDEN)


class ResourceNotFoundException(SurgeryException):
    def __init__(self, message="資源不存在"):
        super().__init__("404", message, status.HTTP_404_NOT_FOUND)


class BusinessException(SurgeryException):
    def __init__(self, message, code="400"):
        super().__init__(code, message, status.HTTP_400_BAD_REQUEST)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, SurgeryException):
        return JsonResponse({
            'code': exc.code,
            'message': exc.message,
            'data': None
        }, status=exc.status_code)

    if response is not None:
        logger.error(f"API異常: {exc}")

        error_code = "500"
        error_message = "系統錯誤"

        if hasattr(exc, 'detail'):
            error_message = str(exc.detail)

        if hasattr(exc, 'status_code'):
            if exc.status_code == 401:
                error_code = "401"
                error_message = "未認證或認證已過期"
            elif exc.status_code == 403:
                error_code = "403"
                error_message = "權限不足"
            elif exc.status_code == 404:
                error_code = "404"
                error_message = "資源不存在"
            elif exc.status_code == 400:
                error_code = "400"
                error_message = str(exc.detail)

        return JsonResponse({
            'code': error_code,
            'message': error_message,
            'data': None
        }, status=response.status_code)

    logger.exception(f"未處理的異常: {exc}")
    return JsonResponse({
        'code': '500',
        'message': '系統內部錯誤',
        'data': None
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
