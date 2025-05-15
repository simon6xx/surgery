from core.serializers.base import AutoModelSerializer
from .models import *


class UserSerializer(AutoModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PermissionSerializer(AutoModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class GroupSerializer(AutoModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
