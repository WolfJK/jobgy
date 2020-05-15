from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User, AbstractUser, Group
# Create your models here.


class GroupInfo(models.Model):
    type_list = (
        ('doer', 1),
        ('opera', 2),
        ('produ', 3),
        ('tester', 4)
    )
    name = models.CharField(unique=True, max_length=50)
    type = models.IntegerField(choices=type_list)

    class Meta:
        abstract = False
        indexes = [
            models.Index(fields=['type'])
        ]
        db_table = 'groupinfo'


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

