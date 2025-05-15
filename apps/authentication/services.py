import json

import bcrypt
from django.conf import settings

from core.common.exceptions import *
from core.jwt.jwt import generate_jwt
from core.utils.redis_client import redis_client
from .models import User, Permission, UserPermission, GroupUser, GroupPermission
from .serializers import PermissionSerializer


class AuthService:
    @staticmethod
    def login(username, password):
        """
        登录
        :param username: 用户名
        :param password: 密码
        :return:
        """
        if not username or not password:
            raise BusinessException("用戶名和密碼不能為空")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ResourceNotFoundException("用戶不存在")

        stored_password = user.password

        # sso生成用户的密码是使用的 spring security 的 BCrypt（保持和sso的密码生成策略一致）
        if stored_password.startswith(('$2a$', '$2b$', '$2y$')):
            is_valid = bcrypt.checkpw(password.encode(), stored_password.encode())
        else:
            is_valid = (stored_password == password)

        if not is_valid:
            raise AuthenticationFailedException("用戶名或密碼錯誤")

        # 权限和JWT生成
        payload = {
            "user_id": user.id,
            "username": user.username,
            "user_type": user.user_type,
        }

        permissions = AuthService.get_user_permissions(user.id)
        permission_codes = [p.detail for p in permissions]
        # 序列化
        permission_serializer = PermissionSerializer(permissions, many=True)
        permission_data = permission_serializer.data

        jwt_token = generate_jwt(payload)

        user_data = {
            "user_id": user.id,
            "username": user.username,
            "user_type": user.user_type,
            "permissions": permission_codes
        }
        redis_client.setex(f"user:{user.id}", settings.JWT_EXPIRATION_DELTA, json.dumps(user_data))

        return {
            "authorization": jwt_token,
            "user_type": user.user_type,
            "permissions": permission_data
        }

    @staticmethod
    def get_user_permissions(user_id):
        """
        获取用户权限
        :param user_id: 用户id
        :return: permission模型对象集合
        """
        user_permission_ids = UserPermission.objects.filter(user_id=user_id).values_list('permission_id', flat=True)

        group_ids = GroupUser.objects.filter(user_id=user_id).values_list('group_id', flat=True)
        group_permission_ids = GroupPermission.objects.filter(group_id__in=group_ids).values_list('permission_id',
                                                                                                  flat=True)
        all_permission_ids = list(set(user_permission_ids) | set(group_permission_ids))

        if not all_permission_ids:
            return Permission.objects.none()

        return Permission.objects.filter(id__in=all_permission_ids)

    @staticmethod
    def logout(current_user):
        redis_client.delete(f"user:{current_user.get('id')}")
        return True
