from django.db.models import Q
from rest_framework import serializers


from goods.models import Goods

from goods.models import GoodsCategory


# class GoodsSerializer(serializers.Serializer):
#     name = serializers.CharField(required=True,max_length=100)
#     click_num=serializers.IntegerField(default=0)
#     goods_front_image=serializers.ImageField()
from goods.models import GoodsImage

from goods.models import Banner

from goods.models import GoodsCategoryBrand

from goods.models import IndexAD


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


class BannerSerializer(serializers.ModelSerializer):
    '''轮播图'''

    class Meta:
        model = Banner
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    #宣传商标

    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


class IndexCategorySerializer(serializers.ModelSerializer):
    #某个大类的商标，可以有多个商标，一对多的关系
    brands = BrandSerializer(many=True)
    # good有一个外键category，但这个外键指向的是三级类，直接反向通过外键category（三级类），取某个大类下面的商品是取不出来的
    goods = serializers.SerializerMethodField()
    # 在parent_category字段中定义的related_name="sub_cat"
    # 取二级商品分类
    sub_cat = CategorySerializer2(many=True)
    # 广告商品
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAD.objects.filter(category_id=obj.id, )
        if ad_goods:
            #取到这个商品Queryset[0]
            good_ins = ad_goods[0].goods
            #在serializer里面调用serializer的话，就要添加一个参数context（上下文request）,嵌套serializer必须加
            # serializer返回的时候一定要加 “.data” ，这样才是json数据
            goods_json = GoodsSerializer(good_ins, many=False, context={'request': self.context['request']}).data
        return goods_json


        #自定义获取方法
    def get_goods(self, obj):
        # 将这个商品相关父类子类等都可以进行匹配
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = "__all__"