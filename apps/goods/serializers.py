

from rest_framework import serializers


from goods.models import Goods

from goods.models import GoodsCategory


# class GoodsSerializer(serializers.Serializer):
#     name = serializers.CharField(required=True,max_length=100)
#     click_num=serializers.IntegerField(default=0)
#     goods_front_image=serializers.ImageField()
from goods.models import GoodsImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=GoodsCategory
        fields = '__all__'






class CategorySerializer3(serializers.ModelSerializer):
    '''三级分类'''
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    '''
    二级分类
    '''
    #在parent_category字段中定义的related_name="sub_cat"
    sub_cat = CategorySerializer3(many=True)



    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    商品一级类别序列化
    """
    sub_cat = CategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=GoodsImage
        fields=("image",)


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = '__all__'
