import time
from random import Random

from rest_framework import serializers

from goods.models import Goods
from goods.serializers import GoodsSerializer
from trade.models import shoppingCar, OrderGoods, OrderInfo

from utils.alipay import AliPay

from myshop.settings import private_key_path, ali_pub_key_path


class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)
    class Meta:
        model = shoppingCar
        fields = '__all__'



class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True,min_value=1,
                                    error_messages={
                                        'min_value':'商品数量不能小于1',
                                        'required':'请选择购买数量'
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True,queryset=Goods.objects.all())
    # 判断购物车里面是否有商品
    def create(self, validated_data):
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']

        existed = shoppingCar.objects.filter(user=user,goods=goods)

        if existed:
            existed = existed[0]
            existed.nums +=nums
        else:
            shoppingCar.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
#         修改商品数量
        instance.nums = validated_data['nums']
        instance.save()
        return instance


class OrderGoodsSerialzier(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)
    #阿里订单 url
    alipay_url=serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self,obj):

     class Meta:
        model = OrderGoods
        fields = '__all__'



class OrderDetailSerializer(serializers.ModelSerializer):

    #生成的是购物车内的商品 的支付链接！！！

    goods = OrderGoodsSerialzier(many=True)
    # 支付订单的url
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid="2016092500591374",
            app_notify_url="http://212.64.64.114:55555/alipay/return",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://212.64.64.114:55555/alipay/return",
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url
    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    #根据购新增商品，生成新的订单号及相关信息
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    #生成订单时，这些不用提交
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.CharField(read_only=True)
    nonce_str = serializers.CharField(read_only=True)
    pay_type = serializers.CharField(read_only=True)
    #支付订单的url
    alipay_url  = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid="2016092500591374",
            app_notify_url="http://212.64.64.114:55555/alipay/return",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://212.64.64.114:55555/alipay/return",
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url




    def generate_order_sn(self):
        # 当前时间+userid+随机数
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random_ins.randint(10, 99))

        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs


    class Meta:
        model = OrderInfo
        fields = '__all__'