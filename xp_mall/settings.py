# coding:utf-8

import os
import sys
import mysql.connector

# 基础路经
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# 解决linux与windows下sqlite文件路径兼容性
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

# 支付完成后回调域名
DOMAIN = "test.articuly.com:7777"


# 基础配置
class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')
    BASEDIR = basedir
    LOG_FILES_PATH = os.path.join(basedir, "logs")
    CACHE_TYPE = "null"
    CACHE_DIR = os.path.join(basedir, "cache")
    WHOOSHEE_MIN_STRING_LEN = 1

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_FILE_UPLOADER = "admin.ckeditor_upload"
    CKEDITOR_FILE_BROWSER = "admin.ckeditor_browser"

    DROPZONE_MAX_FILE_SIZE = 3
    DROPZONE_MAX_FILES = 30
    MAX_CONTENT_LENGTH = 3000 * 1024
    DROPZONE_ALLOWED_FILE_TYPE = "image"
    DROPZONE_ENABLE_CSRF = True
    DROPZONE_INPUT_NAME = 'upload'
    # 自定义上传类型
    # DROPZONE_ALLOWED_FILE_CUSTOM = True
    # DROPZONE_ALLOWED_FILE_TYPE = "image/*, .pdf"

    XPMALL_GOODS_PER_PAGE = 10
    XPMALL_MANAGE_GOODS_PER_PAGE = 5
    XPMALL_SLOW_QUERY_THRESHOLD = 1

    XPMALL_UPLOAD_PATH = os.path.join(BASEDIR, 'uploads')
    XPMALL_ALLOWED_UPLOAD_TYPE = ["image/jpeg", "image/png", "image/gif"]
    XPMALL_IMAGE_SIZE = {'small': 400, 'medium': 800}
    XPMALL_IMAGE_SUFFIX = {
        # 小图后缀
        'small': '_s',
        # 中等图后缀
        'medium': '_m',
    }


# 开发环境配置
class DevelopmentConfig(BaseConfig):
    CKEDITOR_PKG_TYPE = "full"

    # sqlite数据库
    # SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data.db')
    # mysql数据库
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:123456@127.0.0.1/mymall"

    # 支付宝接口配置
    ALIPAY = {
        "DEBUG": True,
        "LOG_PATH": os.path.join("logs/alipay.log"),
        "ALIPAY_SIGN_TYPE": "RSA2",
        # appid 必填
        # appid与私钥，公钥配套，多个appid不要搞混
        "ALIPAY_APP_ID": '2016102500757966',
        # 支付宝密钥证书路径
        "ALIPAY_PRIVATE_KEY_FILE": os.path.join(basedir, "alipay_cert/alipay_private_key"),
        "ALIPAY_PUB_KEY_FILE": os.path.join(basedir, "alipay_cert/alipay_public_key"),
        # 支付成功回调地址
        "ALIPAY_NOTIFY_URL": "http://%s/mall/pay/alipay/notify" % DOMAIN,
        "ALIPAY_RETURN_URL": "http://%s/mall/pay/alipay/return" % DOMAIN,
    }

    # 微信支付接口配置
    WECHAT = {
        # wechat
        # 微信公众号appid与apsecret
        "WECHAT_APPID": "公众号id",
        "WECHAT_APPSECRET": "公众号证书"
    }
    WXPAY = {
        # wechatPay
        # 微信支付应用id与商户id
        "DEBUG": True,
        # 商户ID
        "MCH_ID": "商户ID",
        # 商户号绑定的APPID(公众号id)
        "APP_ID": "",
        # 密钥
        "KEY": "密钥",
        # 公钥与私钥证书路径，通过微信支付工具生成
        "WXPAY_CERT_FILE": os.path.join(basedir, "wechat_cert/apiclient_cert.pem"),
        "WXPAY_CERT_KEY": os.path.join(basedir, "wechat_cert/apiclient_key.pem"),
        # 后台通知
        "WXPAY_NOTIFY_URL": "http://%s/mall/pay/wxpay/notify" % DOMAIN
    }


# 生产环境配置
class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))
    APP_ID = os.getenv('APP_ID')
    APP_TOKEN = os.getenv('APPTOKEN')
    CACHE_TYPE = "filesystem"

    # 支付宝接口配置
    ALIPAY = {
        "DEBUG": False,
        "ALIPAY_SIGN_TYPE": "RSA2",
        "ALIPAY_APP_ID": '',
        "ALIPAY_APP_KEY_FILE": os.path.join(basedir, "alipay_cert/alipay_public_key"),
        "ALIPAY_NOTIFY_URL": "",
        "ALIPAY_RETURN_URL": "",
    }

    # 微信支付接口配置
    WECHAT = {
        "WECHAT_APPID": "",
        "WECHAT_APPSECRET": ""
    }
    WXPAY = {
        "APP_ID": "",
        "MCH_ID": "",
        "KEY": "",
        # 公钥与私钥
        "WXPAY_CERT_FILE": "",
        "WXPAY_CERT_KEY": ""
    }


config = {'development': DevelopmentConfig, 'production': ProductionConfig}
