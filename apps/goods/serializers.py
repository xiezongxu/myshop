

from rest_framework import serializers

# class GoodsSerializer(serializers.Serializer):
#     name = serializers.CharField(required=True,max_length=100)
#     click_num=serializers.IntegerField(default=0)
#     goods_front_image=serializers.ImageField()
from goods.models import Goods

from goods.models import GoodsCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=GoodsCategory
        fields = '__all__'

class GoodsSerializer(serializers.ModelSerializer):

    category= CategorySerializer()
    class Meta:
        model=Goods
        fields='__all__'