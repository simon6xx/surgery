from apps.authentication.models import User
from apps.authentication.serializers import UserSerializer
from core.common.exceptions import *
from core.jwt.jwt import verify_jwt


class CurrentUserUtil:

    @staticmethod
    def get_current_user(request):
        """
        根据JWT返回当前登录用户信息（如果是权限接口，还可以从request.user_data里面取数据，避免重复查询数据库）
        """
        token = request.headers.get('Authorization')
        if not token:
            raise AuthenticationFailedException("缺少授權信息")

        try:
            payload = verify_jwt(token)
            user_id = payload.get('user_id')
            if not user_id:
                raise AuthenticationFailedException("JWT中缺少user_id")

            try:
                user = User.objects.get(id=user_id)
                return UserSerializer(user).data
            except User.DoesNotExist:
                raise ResourceNotFoundException("使用者不存在")


        except AuthenticationFailedException:
            raise

        except Exception as e:
            raise AuthenticationFailedException(f"Token 驗證失敗: {str(e)}")
