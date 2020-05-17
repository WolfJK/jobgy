
import time
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone

class BlockedIpMiddleware(MiddlewareMixin):
    """中间件类：IP"""

    def process_request(self, request):
        """
        :param request: obj
        :return: response
        """
        if request.method == 'POST':
            api_param = '&'.join([i + '|' + j for i, j in request.POST.items()])
            api_user = request.POST.get('username')
        else:
            api_param, api_user = '', ''
        api_info = dict(
            api_curr = getTime(),
            api_method = request.method,
            api_path = request.path,
            api_user = api_user,
            api_ip = request.META['REMOTE_ADDR'],
            api_param = api_param
        )
        print('---------------------', api_info)



def getTime(ft="%Y-%m-%d %H-%M-%S"):
    """
    返回当前时间
    :param ft: 时间格式 2019-10-09 12:01:08
    :return:
    """
    return timezone.localtime().strftime(ft)
