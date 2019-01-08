"""myshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

import xadmin
from goods.views import GoodsListViewSet

from goods.views import CategoryViewSet

from users.views import SmsCodeViewset,UserViewset

from user_operation.views import UserFavViewset

from user_operation.views import LeavingMessageViewset

from user_operation.views import AddressViewset

from trade.views import ShoppingCartViewset

from trade.views import OrderViewset
from myshop.settings import MEDIA_ROOT
from rest_framework.routers import DefaultRouter

router=DefaultRouter()

router.register(r'goods',GoodsListViewSet)
router.register(r'categorys',CategoryViewSet,base_name='categorys')
router.register(r'code',SmsCodeViewset,base_name='code')
router.register(r'users',UserViewset,base_name='users')
router.register(r'userfavs',UserFavViewset,base_name="userfavs")
router.register(r'messages', LeavingMessageViewset, base_name='messages')
router.register(r'address',AddressViewset,base_name='address')
router.register(r'shopcarts', ShoppingCartViewset, base_name="shopcarts")
router.register(r'orders', OrderViewset, base_name="orders")


urlpatterns = [
    path('admin/', admin.site.urls),

    path('ueditor/',include('DjangoUeditor.urls')),
    path('xadmin/',xadmin.site.urls),

    path('media/<path:path>',serve,{'document_root':MEDIA_ROOT}),
    #path('goods/',GoodsListViewSet.as_view(),name='goods-list'),

    path('docs',include_docs_urls(title='cms1')),
    path('api-auth/',include('rest_framework.urls')),
    re_path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('login/', obtain_jwt_token ),

]
