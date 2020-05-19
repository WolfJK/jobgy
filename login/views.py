from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from login import models
from django.contrib import auth
from django.conf import settings
from django.core import signing
from django.core.paginator import Paginator
import base64
import redis
import logging
import hashlib
from celerytask.tasks import taskWork

logger = logging.getLogger(__name__)

class Error(Exception):
    def __init__(self, f):
        super(Error, self).__init__()
        print(f)


def makeToken():
    header = {
        "typ": "JWT",
        "alg": "HS256"
    }
    payload = {
        'iss': 'publisher',
        'sub': 'sub',
        'aud': 'aud',
        'exp': settings.SESSION_COOKIE_AGE,
        'nbf': 'nbf',
        'iat': '2019-10-10',
        'jti': 'jsnhas09',
        'jwt_secret_key': settings.SECRET_KEY,
    }
    bas = base64.b64encode(base64.b64encode(str(header).encode('ascii')) + base64.b64encode(str(payload).encode('ascii')))
    mdstr = hashlib.md5(settings.SECRET_KEY.encode('ascii'))
    mdstr.update(bas)
    token = mdstr.hexdigest()
    print('token', token)
    return token


def login(request):
    logger.info('login.views.login()')
    data = dict(
        code=0,
        msg='failed'
    )
    # cookies = request.get_signed_cookie('k', salt='zhanggen')
    if request.method == 'GET':
        return JsonResponse(data)
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 如果已登录
        to = request.session.get('token')
        if to:
            logger.info('==========已经登录===============')
            empno = request.POST.get('empno')
            num = request.POST.get('num', 1)
            if empno is not None :
                empno = empno if empno else []
                
                infos = selectUserInfo(empno, int(num))
                data['msg'] = 'success'
                data['infos'] = infos
                #  当用户传参 empno 查询 数据时，执行异步处理
                taskWork.delay(user=to, empno=empno)
                logger.info('发送邮件成功')
                print('发送邮件成功')

        else:
            try:
                obj = models.EmpUserInfo.objects.get(name=username)
                resule = auth.authenticate(request, username=username, password=password)
                data['msg'] = 'success'
                t = makeToken()
                request.session['token'] = t

                auth.login(request, obj, )
                for i, j in request.session.items():
                    print('request.session', i, j)
                data['token'] = t
            except Exception as e:
                raise Error('登录失败')
        return JsonResponse(data)


def register(request):

    return render(request, 'index.html')


def selectUserInfo(indes, num):
    l = list()
    
    if not indes:
        qs = models.EmpUserInfo.objects.all()
    else:

        qs = models.EmpUserInfo.objects.filter(empno__in=indes)
    for q in qs:
        ds = dict(empno=q.empno, name=q.name)
        logger.info(q.name)
        gruoup_nmae = selectGroupInfo(q.name)

        ds['Groupname'] = gruoup_nmae
        l.append(ds)
    data = Paginator(l, 5).get_page(num)
    return data


def selectGroupInfo(n):
    try:
        qs = models.GroupInfo.objects.get(name=n)
        name = models.GroupInfo.type_list[qs.type][1]
    except models.GroupInfo.DoesNotExist as e:
        raise Error('数据不存在')
    return name
