import django_filters

from .models import Goods
from django.db.models import Q

class GoodsFilter(django_filters.rest_framework.FilterSet):
    '''
    商品过滤的类
    '''
    #两个参数，name是要过滤的字段，lookup是执行的行为，‘小与等于本店价格’
    pricemin = django_filters.NumberFilter(name="shop_price", lookup_expr='gte',help_text='最小价格')
    pricemax = django_filters.NumberFilter(name="shop_price", lookup_expr='lte')




    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax',]