import sys,os

#获取当前路径
pwd=os.path.dirname(os.path.realpath(__file__))

#获取项目的根目录
sys.path.append(pad+'../')

#参照manage.py获取当前django的环境变量配置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

import django
django.setup()

from goods.models import GoodsCategory
from db_tools.data.product_data import row_data