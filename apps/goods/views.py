from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView
from .serializers import GoodsSerializer

from .filters import GoodsFilter
from .models import Goods
from rest_framework.response import Response

from rest_framework.pagination import PageNumberPagination

from rest_framework import mixins, viewsets
from rest_framework import generics


class GoodsPagination(PageNumberPagination):
    page_size=5
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 120



class GoodsListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    '商品列表页'

    #这里必须要定义一个默认的排序,否则会报错
    queryset = Goods.objects.all().order_by('id')
    # 分页
    pagination_class = GoodsPagination
    serializer_class = GoodsSerializer
    filter_backends = (DjangoFilterBackend,)

    # 设置filter的类为我们自定义的类
    filter_class = GoodsFilter

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)


    # def get(self,request,format=None):
    #     goods=Goods.objects.all()
    #     goods_serialzer = GoodsSerializer(goods,many=True)
    #     return Response(goods_serialzer.data)
