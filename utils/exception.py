import time
import logging
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.exceptions import ValidationError
from rest_framework import status
from utils.response import HDResponse, HD_HTTP_500_INTERNAL_SERVER_ERROR, HD_HTTP_400_BAD_REQUEST


log = logging.getLogger(__name__)


def exception_handler(exc, context):
    """自定义处理异常函数"""

    response = drf_exception_handler(exc, context)

    # 如果类型为ValidationError代表参数验证出错
    if isinstance(exc, ValidationError):
        http_status = response.status_code
        if isinstance(response.data, dict):
            # 提取错误信息如：{'provider': [ErrorDetail(string='请提供平台供应商', code='required')]}
            # noinspection PyBroadException
            try:
                data_message = str(list(dict(response.data).values())[0][0])
            except Exception:
                data_message = '未找到（服务器找不到请求）'
        elif isinstance(response.data, list):
            # noinspection PyBroadException
            try:
                data_message = response.data[0]
            except Exception:
                data_message = '未找到（服务器找不到请求）'
        else:
            data_message = '参数有误'

        log.debug(data_message)
        return HDResponse(data_status=HD_HTTP_400_BAD_REQUEST, data_message=data_message, http_status=http_status, exception=True)

    # 为空，就是drf框架处理不了的异常
    if response is None:
        # time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # print('\n\n{}\nview: {}\nmethod: {}\nexc: {}\n\n'.format(time_now, context['view'], context['request'].method, exc))

        log.debug('view: {}\nmethod: {}\nexc: {}'.format(context['view'], context['request'].method, exc))
        return HDResponse(data_status=HD_HTTP_500_INTERNAL_SERVER_ERROR, data_message='服务器错误', http_status=HD_HTTP_500_INTERNAL_SERVER_ERROR, exception=True)

    else:
        http_status = response.status_code

        if http_status == status.HTTP_400_BAD_REQUEST:
            data_message = '（错误请求）服务器不理解请求的语法'

        elif http_status == status.HTTP_401_UNAUTHORIZED:
            data_message = '（未授权）请求要求身份验证'

        elif http_status == status.HTTP_403_FORBIDDEN:
            data_message = '（禁止）服务器拒绝请求'

        elif http_status == status.HTTP_404_NOT_FOUND:
            try:
                data_message = response.data.get('detail')
            except KeyError:
                data_message = '未找到（服务器找不到请求）'

        elif http_status == status.HTTP_405_METHOD_NOT_ALLOWED:
            data_message = '（方法禁用）禁用请求中指定的方法'

        elif http_status >= status.HTTP_500_INTERNAL_SERVER_ERROR:
            data_message = '服务器错误'

        else:
            data_message = '未知错误'

    log.debug(data_message)
    return HDResponse(data_status=http_status, data_message=data_message, http_status=http_status, exception=True)
