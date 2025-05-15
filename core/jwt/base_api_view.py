from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class BaseAPIView(APIView):
    # 默认跳过 DRF 的权限校验
    permission_classes = [AllowAny]
