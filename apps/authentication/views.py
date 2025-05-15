import json
import logging

from django.utils.decorators import method_decorator

from core.common.exceptions import BusinessException
from core.common.response import success_response
from core.decorators.permission import permission_required
from core.jwt.base_api_view import BaseAPIView
from core.utils.current_user import CurrentUserUtil
from .models import User
from .serializers import UserSerializer
from .services import AuthService

logger = logging.getLogger('surgery')


class LoginView(BaseAPIView):
    def post(self, request, *args, **kwargs):
        try:
            if request.body:
                # x-www-form-urlencoded
                data = request.data
            else:
                data = request.POST or request.data
        except json.JSONDecodeError:
            data = request.POST or request.data

        username = data.get("username")
        password = data.get("password")

        return success_response(AuthService.login(username, password))


class LogoutView(BaseAPIView):
    def delete(self, request, *args, **kwargs):
        current_user = CurrentUserUtil.get_current_user(request)
        AuthService.logout(current_user)

        return success_response()


class UserInfoView(BaseAPIView):
    def get(self, request, *args, **kwargs):
        current_user = CurrentUserUtil.get_current_user(request)
        return success_response(current_user)


@method_decorator(permission_required('user:list'), name='dispatch')
class UserListView(BaseAPIView):
    def get(self, request, *args, **kwargs):
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return success_response(serializer.data)
        except Exception as e:
            logger.error(f"获取用户列表失败: {str(e)}")
            raise BusinessException("獲取用戶列表失敗，請稍後重試")
