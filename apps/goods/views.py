from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView
from .serializers import GoodsSerializer, CategorySerializer, BannerSerializer, IndexCategorySerializer

from .filters import GoodsFilter
from .models import Goods, GoodsCategory, Banner
from rest_framework.response import Response

from rest_framework.pagination import PageNumberPagination

from rest_framework import mixins, viewsets,filters
from rest_framework import generics


class GoodsPagination(PageNumberPagination):
    page_size=12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100



class GoodsListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    '''
    list:
        商品列表,分页,搜索,过滤,排序

    retrieve: 获取商品详情
    '''


    #这里必须要定义一个默认的排序,否则会报错
    queryset = Goods.objects.all().order_by('id')
    # 分页
    pagination_class = GoodsPagination
    serializer_class = GoodsSerializer
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)

    # 设置filter的类为我们自定义的类
    filter_class = GoodsFilter
    search_fields = ('name','goods_brief','goods_desc')
    ordering_fields=('sold_num','add_time')

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)


    # def get(self,request,format=None):
    #     goods=Goods.objects.all()
    #     goods_serialzer = GoodsSerializer(goods,many=True)
    #     return Response(goods_serialzer.data)


class CategoryViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer



class BannerViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    '''首页轮播图'''

    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商品分类数据
    """
    # 获取is_tab=True（导航栏）里面的分类下的商品数据
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorySerializer







