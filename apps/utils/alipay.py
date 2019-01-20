import json
from datetime importdatetime
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64decode,b64decode
from urllib.parse import quote_plus,urlparse,parse_qs
from urllib.request import urlopen
from base64 import decodebytes,encodebytes

class AliPay(object):
    '''支付宝支付接口'''

    def __init__(self,appid,app_notify_url,app_private_key_path,alipay_public_key_path,
                 return_url,debug=False):
        self.appid=appid
        self.app_notify_url=app_notify_url
        #私钥
        self.app_private_key_path=app_private_key_path
        self.app_private_key=None
        self.return_url = return_url
        with open(self.app_private_key_path)as fp:
            self.app_private_key=RSA.importKey(fp.read())
        #公钥
        self.alipay_pub_key_path = alipay_public_key_path
        with open(self.alipay_pub_key_path)as fp:
            self.alipay_pub_key_path = RSA.import_key(fp.read())

        if debug is True:
            self.__gateway="https://openapi.alipaydev.com/gateway.do"
        else:
            self.__gateway = "https://openapi.alipay.com/gateway.do"


    def direct_pay(self,subject,out_trade_no,total_amount,return_url=None,**kwargs):

        biz_content={
            "subject":subject,
            "out_trade_no":out_trade_no,
            "total_amount":total_amount,
            "product_code":"FAST_INSTANT_TRADE_PAY",

        }
        biz_content.update(kwargs)
        data = self.build_body("alipay.trade.page.pay",biz_content,self.return_url)
        return self.sign_data(data)

