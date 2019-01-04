import re
from datetime import datetime,timedelta
from myshop.settings import REGEX_MOBILE
from users.models import VerifyCode
from rest_framework import serializers
from django.contrib.auth import get_user_model
User=get_user_model()

class SmsSerializer(serializers.Serializer):
    mobile= serializers.CharField(max_length=11)

