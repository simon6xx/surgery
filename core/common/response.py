from rest_framework import status
from rest_framework.response import Response


class ResultDTO:
    def __init__(self, code, message, data=None):
        self.code = code
        self.message = message
        self.data = data

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message,
            "data": self.data
        }

    @staticmethod
    def success(data=None, message="success", code="200"):
        return ResultDTO(code=code, message=message, data=data)

    @staticmethod
    def error(message="error", code="400", data=None):
        return ResultDTO(code=code, message=message, data=data)


def success_response(data=None, message="success", code="200", status_code=status.HTTP_200_OK):
    """
    返回标准成功响应
    :param data: 返回数据
    :param message: 消息内容（可选）
    :param code: 自定义返回码（默认为200）
    :param status_code: HTTP状态码（默认为200）
    """
    result = ResultDTO.success(data=data, message=message, code=code)
    return Response(result.to_dict(), status=status_code)


def error_response(message="error", code="400", data=None, status_code=status.HTTP_400_BAD_REQUEST):
    """
    返回标准失败响应
    :param message: 错误信息（可选）
    :param code: 自定义返回码（默认为400）
    :param data: 返回数据（可选，通常为None或额外错误上下文）
    :param status_code: HTTP状态码（默认为400）
    """
    result = ResultDTO.error(message=message, code=code, data=data)
    return Response(result.to_dict(), status=status_code)
