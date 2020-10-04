# coding:utf-8
import logging
import traceback

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.FileItem import FileItem
from alipay.aop.api.domain.AlipayTradeAppPayModel import AlipayTradeAppPayModel
# 网页支付对象
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.AlipayTradePayModel import AlipayTradePayModel
from alipay.aop.api.domain.GoodsDetail import GoodsDetail
from alipay.aop.api.domain.SettleDetailInfo import SettleDetailInfo
from alipay.aop.api.domain.SettleInfo import SettleInfo
from alipay.aop.api.domain.SubMerchant import SubMerchant
from alipay.aop.api.request.AlipayOfflineMaterialImageUploadRequest import AlipayOfflineMaterialImageUploadRequest
from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest
# 网页支付请求
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.request.AlipayTradePayRequest import AlipayTradePayRequest
from alipay.aop.api.response.AlipayOfflineMaterialImageUploadResponse import AlipayOfflineMaterialImageUploadResponse
from alipay.aop.api.response.AlipayTradePayResponse import AlipayTradePayResponse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a', )
logger = logging.getLogger('')

if __name__ == '__main__':
    """
    设置配置，包括支付宝网关地址、app_id、应用私钥、支付宝公钥等，其他配置值可以查看AlipayClientConfig的定义。
    """
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = 'https://openapi.alipay.com/gateway.do'
    alipay_client_config.app_id = '2021001198627524'
    alipay_client_config.app_private_key = 'MIIEpQIBAAKCAQEAuys0k4PSwrwNQNwS5YFuldJ7t08CKelXPihhDNCClKf39yVaVvrMjvu5kJdHfppIab996Eniu+P9xWk4mGt5QLRnGtBcwCDVgQzo6Yu1of0Ys6QHqjcm61OZ1LFR64niNU5nsNfe5YgcsjI1In2JUHEiNPedRUqEOv/37CWHFIuCv1TlD4F+BvEvM83RKq5riICCCBJAAVje1mXO6sCLsyJDbFFGQPe20bJg0q1+3iCTOGfJ2jH5RaISstbcfCXPzM0yOaxEhy4fbnGa2tD0jtwDBFS7Gs5xLifVHyphYH6wH6eKxKzcIyi0NqN2vw9mdnhWqARRb8b2gewdZraMwQIDAQABAoIBADhaZdYUVpyzKfphSH85XSZW3VDvxOMBknbwiWfmT6qaeBo9cNnHYVebit9x7OC9axgLw8jwlgekOX/6kkOx+Cv3JSP5oDNor1/Pl0DaA7HmFk3gET66pEkuPp6/VL7qIOWT2bxxAndxZ9JvM3hS+8jwhzATbZKzQOTStL6w/d69LquYjf5HrViY0nca0NEc26EhPfBtXwAFHNhYf6pF1Nlrmw2S6plbAocIppJl2uFpvOzwxP/aljeZe+HbKwLHOaK4MxVRv02arPCGNA0+gxAoE6KKYKRVMkIQIhQNu14v4VSpYvmA0MNiPUzLgIXL0JAv0rSwoDbQoMQYXL0cuJECgYEA3H1FDIPE3v+FNN+QyNcuB//06RWn5k+pjP2z4WB5VtC8XfSVOTWn0VfHcmxOy2Jk5gljDtT1LzwiE8JVabSjXW0bH7S9cLtonw+z7h1vu5T1MiKuMzTW7XY4Ck4IkcSjnZTzR2oRiinkdrMMc5TRMcFYLXE2XpW3/S1SG2axb+sCgYEA2VAitxajnMs/NEwS/46JaLJ3KalbDHSnhjCj6n6Hxp3JUmF/b1SekkLrU1lJaEvgpcee8EHOBH6vBRJakUTBi9RH3vepsdAa42WaK7wnJcrKsPvU4lEbZHyxaYK4eIeFwz0V1Md8ab08jQfBzxjaiT6/SWHwMBh6TI+yINvUdwMCgYEAw9Qi4pWZ4jFxvt8debPb91D21ZndUKnKPiYKgI6t1lR4KL6VVoV4Mm9S/iaB6RPP55vItiCgTz6KSaBdOhAs1EqWP5fIdXqN1lAdD8xnM2R+TfQNYf95MNjBty1NYSIT616in/ft8hd5CY/G7FTtY9KEHYAiuOkiy6NX/Gw+BdcCgYEA16lmekq2XnF6LR1eMU40YbnS9n6CxC603kBBPAMMHfkTBXWKsWLJ558PyWyvpBjBPeSIgCjeGqnaaW8YgFg6t9kY5lbkinlbZda8FLEqLKA/XTrevyb8x1HUA0Deb4cXIXXqx3qdppZNlCxhk3Q31MJ3tYzDgAeav4ZPobpn9R8CgYEAvikslWd2OB8jrZ2NMh7ovHMS+hRYeNHGkP2U9nfsVVO1XR0nUtdAwIgj/rrpcKFlg3MN5bIV9rfDMSUrjh2yLFu+S7Rq2bwgYkLg4vMTdh+AvvMRKyNGYOqqWY1f5p7A9jIsgVtc+GeSYePyd0F57NWj4R9IgxZbqEer6KLH2IQ='
    alipay_client_config.alipay_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAiWMUFAovq02SvXKyQPE20tnX9+irJtNDZqZnQCjiBULf9+laP/xeLopV+Nr2Dy6fYqfFFQ2jIqqbf/8ZXfq5tBCkwZ2ta+0mLVXbn0ZgUzUqLMVMl4SAGlJ7kgatUD0V+fdPXwhOwwX/r99wEZyBJalt/dhAzEZyS0KGgcVRzTyzpj6PEgvPwrpDzetTs3/Ot3M/aukt/h1XcJoRFbHOz9Cu3vwerzX018aHynUXR2tJHY+MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAl0zdZkgculoIuYvoAXFUmTaT5MTB3CYVdLMSBH7THC6Mo6tW8x/QW0QcVd82CC2s3R1mPS02qhkwQaleQAEWx0htXbmPq/J4eonUdIK1Gbp/rvB9eAyvVBTdUHJz7MT5bYjv8dDxr2ZfNo6EKM6ndFlMHp/scHaMnQqmVJgZSgi+gUkQwjDP/jR0rEkWF01YTcCrxIxTyoVJsfG46PO2dia4Ip45IBRhhO7QrUL9OIexgr5WH0O0vMvKYay0ParXiVL7U1E5d6pUUPDJwbTu7Nz6D4OiVrbqEwz7sTH1979sIPTEopRWcK4Y/BEwNTiba/Wa2PWWDjPxkeqzIQqkCwIDAQAB'

    """
    得到客户端对象。
    注意，一个alipay_client_config对象对应一个DefaultAlipayClient，定义DefaultAlipayClient对象后，alipay_client_config不得修改，如果想使用不同的配置，请定义不同的DefaultAlipayClient。
    logger参数用于打印日志，不传则不打印，建议传递。
    """
    client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)

    """
    系统接口示例：alipay.trade.pay
    """
    # 对照接口文档，构造请求对象
    model = AlipayTradePayModel()

    #  支付授权码
    model.auth_code = "282877775259787048"

    # 订单描述 可选
    model.body = "Iphone6 16G"
    # goods_list 订单所含商品列表 可选
    goods_list = list()
    goods1 = GoodsDetail()
    goods1.goods_id = "apple-01"
    goods1.goods_name = "ipad"
    goods1.price = 10
    goods1.quantity = 1
    goods_list.append(goods1)
    model.goods_detail = goods_list

    # 商户操作员编号 可选
    model.operator_id = "yx_001"

    # 商户订单号 必填
    model.out_trade_no = "20180510AB014"

    # 产品码 可选
    model.product_code = "FACE_TO_FACE_PAYMENT"

    # 支付场景 条码支付 bar_code ,声波支付 wave_code
    model.scene = "bar_code"

    # 商户门店编号
    model.store_id = ""
    # 订单标题
    model.subject = "huabeitest"

    # 订单最晚支付时间 m、h、d, 整数值，当天1c，0点关闭
    model.timeout_express = "90m"

    # 订单总金额 ，精确到小数点后两位
    model.total_amount = 1

    request = AlipayTradePayRequest(biz_model=model)
    # 如果有auth_token、app_auth_token等其他公共参数，放在udf_params中
    # udf_params = dict()
    # from alipay.aop.api.constant.ParamConstants import *
    # udf_params[P_APP_AUTH_TOKEN] = "xxxxxxx"
    # request.udf_params = udf_params
    # 执行请求，执行过程中如果发生异常，会抛出，请打印异常栈
    response_content = None
    try:
        response_content = client.execute(request)
    except Exception as e:
        print(traceback.format_exc())
    if not response_content:
        print("failed execute")
    else:
        response = AlipayTradePayResponse()
        # 解析响应结果
        response.parse_response_content(response_content)
        if response.is_success():
            # 如果业务成功，则通过respnse属性获取需要的值
            print("get response trade_no:" + response.trade_no)
        else:
            # 如果业务失败，则从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
            print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)

    """
    带文件的系统接口示例：alipay.offline.material.image.upload
    """
    # 如果没有找到对应Model类，则直接使用Request类，属性在Request类中
    request = AlipayOfflineMaterialImageUploadRequest()
    request.image_name = "我的店"
    request.image_type = "jpg"
    # 设置文件参数
    f = open(r"F:\Pictures\starnight.jpg", "rb")
    request.image_content = FileItem(file_name="starnight.jpg", file_content=f.read())
    f.close()
    response_content = None
    try:
        response_content = client.execute(request)
    except Exception as e:
        print(traceback.format_exc())
    if not response_content:
        print("failed execute")
    else:
        response = AlipayOfflineMaterialImageUploadResponse()
        response.parse_response_content(response_content)
        if response.is_success():
            print("get response image_url:" + response.image_url)
        else:
            print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)

    """
    页面接口示例：alipay.trade.page.pay
    """
    # 对照接口文档，构造请求对象
    model = AlipayTradePagePayModel()
    model.out_trade_no = "pay201805020000226"
    model.total_amount = 50
    model.subject = "测试"
    model.body = "支付宝测试"
    model.product_code = "FAST_INSTANT_TRADE_PAY"
    settle_detail_info = SettleDetailInfo()
    settle_detail_info.amount = 50
    settle_detail_info.trans_in_type = "userId"
    settle_detail_info.trans_in = "2088302300165604"
    settle_detail_infos = list()
    settle_detail_infos.append(settle_detail_info)
    settle_info = SettleInfo()
    settle_info.settle_detail_infos = settle_detail_infos
    model.settle_info = settle_info
    sub_merchant = SubMerchant()
    sub_merchant.merchant_id = "2088301300153242"
    model.sub_merchant = sub_merchant
    request = AlipayTradePagePayRequest(biz_model=model)
    # 得到构造的请求，如果http_method是GET，则是一个带完成请求参数的url，如果http_method是POST，则是一段HTML表单片段
    response = client.page_execute(request, http_method="GET")
    print("alipay.trade.page.pay response:" + response)

    """
    构造唤起支付宝客户端支付时传递的请求串示例：alipay.trade.app.pay
    """
    model = AlipayTradeAppPayModel()
    model.timeout_express = "90m"
    model.total_amount = "9.00"
    model.seller_id = "2088301194649043"
    model.product_code = "QUICK_MSECURITY_PAY"
    model.body = "Iphone6 16G"
    model.subject = "iphone"
    model.out_trade_no = "201800000001201"
    request = AlipayTradeAppPayRequest(biz_model=model)
    response = client.sdk_execute(request)
    print("alipay.trade.app.pay response:" + response)
