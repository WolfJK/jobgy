from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from login.models import EmpUserInfo
from django.contrib import auth

class Error(Exception):
    print('登录失败')


def login(request):
    data = dict(
        code=0,
        msg='success'
    )
    if request.method == 'GET':

        return JsonResponse(data)
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        obj = EmpUserInfo.objects.get(name=username)
        try:
            resule = auth.authenticate(request, username=username, password=password)
        except Exception as e:
            raise Error
        print('*'*10, obj)
        return JsonResponse(data)


def register(request):

    return render(request, 'index.html')