import re
from datetime import datetime,timedelta

from rest_framework.validators import UniqueValidator

from myshop.settings import REGEX_MOBILE
from .models import VerifyCode
from rest_framework import serializers
from django.contrib.auth import get_user_model
User=get_user_model()

class SmsSerializer(serializers.Serializer):
    mobile= serializers.CharField(max_length=11)


class UserRegSerializer(serializers.ModelSerializer):

    # UserProfile中没有code字段，这里需要自定义一个code序列化字段
    code=serializers.CharField(required=True,write_only=True,max_length=4,min_length=4,
                               error_messages={
                                   "blank":"请输入验证码",
                                   "required":"请输入验证码2",
                                   "max_length":"验证码格式错误1",
                                   "min_length":"验证码格式错误2",
                                  },
                                help_text="验证码2")
    #验证code
    def validate_code(self,code):
    # 用户注册，已post方式提交注册信息，post的数据都保存在initial_data里面
    # username就是用户注册的手机号，验证码按添加时间倒序排序，为了后面验证过期，错误等

        verify_records=VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")

        # if verify_records:
        #     last_record = verify_records[0]
        #     five_mintes_ago=datetime.now() - timedelta(hours=0,minutes=5,seconds=0)
        #     if five_mintes_ago > last_record.add_time:
        #         raise serializers.ValidationError("验证码过期")
        #     if last_record.code !=code:
        #         raise serializers.ValidationError("验证码错误2")
        #
        # else:
        #     raise serializers.ValidationError("验证码错误3")



    # 所有字段。attrs是字段验证合法之后返回的总的dict
    def validate(self,attrs):
        attrs["mobile"]=attrs["username"]

        # code是自己添加得，数据库中并没有这个字段，验证完就删除掉
        del attrs["code"]
        return  attrs

    username = serializers.CharField(label="用户名", help_text="用户名3", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    password= serializers.CharField(
        style={'input_type':'password'},write_only=True
    )
    print('password（DRF输入属性）:',password)

    def create(self, validated_data1):
        user=super(UserRegSerializer,self).create(validated_data=validated_data1)
        user.set_password(validated_data1['password'])
        user.save()
        return user


    class Meta:
        model=User
        fields=('username','code','mobile','password')



class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情
    """
    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email","mobile")
