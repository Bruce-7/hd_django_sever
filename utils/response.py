import time
from rest_framework.response import Response
import logging


log = logging.getLogger(__name__)

# 自定义响应数据状态码
HD_HTTP_0_SUCCEED = 0  # 响应成功
HD_HTTP_1_OPERATION_RESOURCE_FAILED = 1  # 操作资源失败
HD_HTTP_400_BAD_REQUEST = 400  # （错误请求） 服务器不理解请求的语法。
HD_HTTP_500_INTERNAL_SERVER_ERROR = 500  # 内部服务器错误


class HDResponse(Response):
    """自定义响应"""

    def __init__(self, data_status=HD_HTTP_0_SUCCEED, data_message='succeed', data_results=None,
                 http_status=None, headers=None, exception=False, **kwargs):
        # 响应数据状态和信息报告
        data = {
            'status': data_status,
            'message': data_message,
        }

        # 响应数据内容
        if data_results is not None:
            data['results'] = data_results

        # 响应的其他内容
        # if kwargs is not None:
        #     for k, v in kwargs.items():
        #         setattr(data, k, v)
        data.update(kwargs)

        log.debug('响应结果: data: {}'.format(data))
        super().__init__(data=data, status=http_status, headers=headers, exception=exception)
