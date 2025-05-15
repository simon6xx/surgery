import json
from functools import wraps

from core.common.exceptions import *
from core.jwt.jwt import verify_jwt
from core.utils.redis_client import redis_client


def permission_required(permission_code):
    """权限检查装饰器"""

    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            # 在 DRF 的类视图中，dispatch方法的request是Django原生HttpRequest对象，它没有headers属性，所有请求头都通过META提供
            token = request.META.get('HTTP_AUTHORIZATION')
            if not token:
                raise AuthenticationFailedException("缺少授權信息")

            try:
                # 解码并验证JWT
                decoded_payload = verify_jwt(token)
                user_id = decoded_payload.get('user_id')
            except Exception as e:
                raise AuthenticationFailedException(f"Token 驗證失敗: {str(e)}")

            cached_user_data = redis_client.get(f"user:{user_id}")
            if not cached_user_data:
                raise AuthenticationFailedException("用戶未登錄或會話已過期")

            user_data = json.loads(cached_user_data)
            # 将用户信息添加到request中，无需重复解析JWT或查询数据库
            request.user_data = user_data

            if user_data.get("user_type") == "ADMINISTRATOR":
                return view_func(request, *args, **kwargs)

            permissions = user_data.get("permissions", [])
            if permission_code in permissions:
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDeniedException("權限不足")

        return wrapped_view

    return decorator
