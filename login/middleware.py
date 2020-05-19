
import time
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
import json 


def parse_body(request):
    try:
        data = json.loads(request.body) if request.body else {}
    except Exception as e:
        data = {_.split('=')[0]: _.split('=')[1] for _ in request.body.decode().split('&')}
    return data

class BlockedIpMiddleware(MiddlewareMixin):
    """中间件类：IP"""

    def process_request(self, request):
        """
        :param request: obj
        :return: response
        """

        api_info = dict(
            api_curr = getTime(),
            api_method = request.method,
            api_path = request.path,
            api_user = request.user,
            api_ip = request.META['REMOTE_ADDR'],
            api_param = parse_body(request)
        )
        log = '{api_curr} {api_method} {api_path} {api_user} {api_ip} {api_param}'.format(**api_info)
        with open('log', 'a+', encoding='utf8') as p:
            p.write(log)



def getTime(ft="%Y-%m-%d %H-%M-%S"):
    """
    返回当前时间
    :param ft: 时间格式 2019-10-09 12:01:08
    :return:
    """
    return timezone.localtime().strftime(ft)
