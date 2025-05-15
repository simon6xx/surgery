import json
import logging
import time

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('surgery')


class RequestLogMiddleware(MiddlewareMixin):
    """
    记录所有请求和响应信息
    """

    def process_request(self, request):
        request.start_time = time.time()

        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                body = json.loads(request.body) if request.body else {}
                # 敏感信息处理
                if 'password' in body:
                    body['password'] = '******'
                request.request_body = body
            except Exception:
                request.request_body = {}

        return None

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time

            log_data = {
                'method': request.method,
                'path': request.path,
                'duration': f"{duration:.2f}s",
                'status': response.status_code,
            }

            if hasattr(request, 'request_body'):
                log_data['request_body'] = request.request_body

            if hasattr(request, 'user_id'):
                log_data['user_id'] = request.user_id

            log_message = f"Request: {json.dumps(log_data)}"
            if 200 <= response.status_code < 400:
                logger.info(log_message)
            else:
                logger.warning(log_message)

        return response
