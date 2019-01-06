from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class UserProfile(AbstractUser):


    name=models.CharField(max_length=30,null=True,verbose_name='姓名')
    birthday=models.DateField(null=True,blank=True,verbose_name='出生日期')
    gender=models.CharField(max_length=6,choices=(('male','男'),('female','女')),default='male')
    mobile=models.CharField(max_length=11,null=True,blank=True,verbose_name='电话1')
    email = models.CharField(max_length=100,null=True,blank=True,verbose_name='邮件')

    class Meta:
        verbose_name='用户'
        verbose_name_plural=verbose_name



class VerifyCode(models.Model):

    code=models.CharField(max_length=10,verbose_name='验证码')
    mobile=models.CharField(max_length=11,verbose_name='手机')
    add_time=models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name='验证码'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.code
