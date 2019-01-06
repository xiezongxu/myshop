from random import choice

from django.shortcuts import render

# Create your views here.
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_encode_handler,jwt_payload_handler
from utils.yunpian import YunPian

from users.models import VerifyCode
from myshop.settings import APIKEY
from .serializers import SmsSerializer, UserRegSerializer

User=get_user_model()

class CustomBackend(ModelBackend):

    def authenticate(self,username=None,password=None,**kwargs):
        try:

            user=User.objects.get(
                Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                    return user
        except Exception as e:
            return None


class SmsCodeViewset(CreateModelMixin,viewsets.GenericViewSet):
    '''手机验证码'''

    serializer_class = SmsSerializer

    def generate_code(self):
        seeds = "1234567890"
        random_str=[]
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def create(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]

        yun_pian=YunPian(APIKEY)
        code=self.generate_code()

        sms_status=yun_pian.send_sms(code=code,mobile=mobile)

        if sms_status["code"] !=0:
            return Response({
                "mobile":sms_status["msg"]
                },status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record=VerifyCode(code=code,mobile=mobile)
            code_record.save
            return Response({
                "mobile":mobile
            },status=status.HTTP_201_CREATED)



class UserViewset(CreateModelMixin,viewsets.GenericViewSet):
    '''
    用户
    '''
    serializer_class = UserRegSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)

        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()





