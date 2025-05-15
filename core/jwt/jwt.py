import datetime
import logging

import jwt
from django.conf import settings

logger = logging.getLogger(__name__)


def generate_jwt(payload):
    """
    生成JWT令牌，使用环境变量.env中的密钥
    """
    try:
        # 设置过期时间
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.JWT_EXPIRATION_DELTA)
        payload['exp'] = expiration_time

        # 生成
        token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )

        # 如果token是bytes类型，转换为字符串
        if isinstance(token, bytes):
            token = token.decode('utf-8')

        return token
    except Exception as e:
        logger.error(f"生成JWT錯誤: {str(e)}")
        raise Exception(f"生成JWT失敗: {str(e)}")


def decode_jwt(token):
    """
    解码JWT
    """
    try:
        # 处理Bearer令牌格式
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        if token.startswith('Bearer '):
            token = token[7:]

        # 使用环境变量中的密钥解码JWT
        decoded = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        return decoded
    except jwt.ExpiredSignatureError:
        logger.error("Token已過期")
        raise Exception("Token已過期")
    except jwt.InvalidTokenError as e:
        logger.error(f"無效的Token: {str(e)}")
        raise Exception(f"無效的Token: {str(e)}")
    except Exception as e:
        logger.error(f"解碼JWT錯誤: {str(e)}")
        raise Exception(f"解碼JWT失敗: {str(e)}")


def verify_jwt(token):
    """
    验证JWT是否有效
    """
    return decode_jwt(token)
