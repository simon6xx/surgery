import json

from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from core.jwt.jwt import verify_jwt
from core.common.exceptions import *
from core.utils.redis_client import redis_client


class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    全局JWT鉴权中间件
    """

    def __init__(self, get_response=None):
        super().__init__(get_response)
        # 白名单
        self.exempt_paths = [
            '/surgery/auth/login',
            '/surgery/auth/logout',
            '/admin',
            '/static',
        ]
        self.async_mode = False

    def is_path_exempt(self, path):
        """检查路径是否免登录"""
        path = path.rstrip('/')
        exempt_paths = [p.rstrip('/') for p in self.exempt_paths]

        return any(path == exempt_path for exempt_path in exempt_paths) or \
            any(path.startswith(exempt_path + '/') for exempt_path in exempt_paths)

    def process_request(self, request):
        """处理请求，进行JWT确认"""
        if self.is_path_exempt(request.path):
            # 保证request.user存在
            request.user = AnonymousUser()
            return None

        token = request.headers.get('Authorization')
        if not token:
            raise AuthenticationFailedException("缺少授權信息")

        try:
            decoded_payload = verify_jwt(token)
            user_id = decoded_payload.get('user_id')
            if not user_id:
                raise AuthenticationFailedException("JWT中缺少user_id")

            cached_user_data = redis_client.get(f"user:{user_id}")
            if not cached_user_data:
                raise AuthenticationFailedException("用戶未登錄或會話已過期")

            request.user_data = json.loads(cached_user_data)
            return None
        except Exception as e:
            raise AuthenticationFailedException(f"Token 驗證失敗: {str(e)}")
