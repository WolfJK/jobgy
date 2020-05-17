from django.test import TestCase

# Create your tests here.



import sys, os
import django
import datetime
pwd = os.path.dirname(os.path.realpath(__file__))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobgy.settings")

django.setup()  # 初始化django路径

from login import models, views

def select():
    # 初始化数据库

    a = models.EmpUserInfo.objects.all()
    # a = models.EmpUserInfo.objects.filter(empno__in=[100, 200, 600])
    b = models.GroupInfo.objects.all()
    for i in a:
        print('0000', i.name, i.empno, i.groups)
    print([[b.name, b.type, type(b.type)] for b in b])
def dat():
    a = models.EmpUserInfo.objects.create(
        username='admin', name='admin', password='123', is_active=1,
                    is_staff=1, is_superuser=1, email='abc@qq.com', first_name='a',
                last_name='b', date_joined=datetime.datetime.now(),empno=100, uuid='jshajsjh',
    )
    b = models.EmpUserInfo.objects.create(
        username='admin1', name='admin1', password='123', is_active=1,
        is_staff=1, is_superuser=1, email='abc@qq.com', first_name='a',
        last_name='b', date_joined=datetime.datetime.now(), empno=200, uuid='jshajsyjhanwh',
    )
    c = models.EmpUserInfo.objects.create(
        username='admin2', name='admi2', password='123', is_active=1,
        is_staff=1, is_superuser=1, email='abc@qq.com', first_name='a',
        last_name='b', date_joined=datetime.datetime.now(), empno=300, uuid='jshajsjh8anwh',
    )
    a.save()
    b.save()
    c.save()

def groups():
    a = models.GroupInfo.objects.create(
        name='admin1', type=1
    )
    b = models.GroupInfo.objects.create(
        name='admin', type=2
    )
    c = models.GroupInfo.objects.create(
        name='admi2', type=2
    )

    # a.save()
    # b.save()
    c.save()



if __name__ == '__main__':
    # groups()
    # dat()
    # select()
    print(views.selectUserInfo([1,200]))
    # print(views.selectGroupInfo('admin11'))