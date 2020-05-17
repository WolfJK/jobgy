from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User, AbstractUser, Group
# Create your models here.



class EmpUserInfo(AbstractUser):
    uuid = models.CharField(max_length=120, primary_key=True)
    name = models.CharField(max_length=20, null=False)
    empno = models.BigIntegerField(
        unique=True, null=False,
        validators=[
            MinValueValidator(50000),
            MinValueValidator(1)
        ])

    class Meta:
        abstract = False
        indexes = [
            models.Index(fields=['empno'])
        ]
        db_table = 'empuserinfo'


class GroupInfo(models.Model):
    type_list = (
        (0, '开发'),
        (1, '运维'),
        (2, '产品'),
        (3, '测试')
    )
    name = models.CharField(unique=True, max_length=50)
    type = models.IntegerField(choices=type_list)
    groups = models.ManyToManyField(EmpUserInfo)

    class Meta:
        abstract = False
        indexes = [
            models.Index(fields=['type'])
        ]
        db_table = 'groupinfo'