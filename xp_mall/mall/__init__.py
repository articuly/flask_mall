# coding:utf-8

from flask import Blueprint, current_app

mall_module = Blueprint('mall', __name__)
from xp_mall.mall.goods import *
from xp_mall.mall.order import *


# 商城信息上下文管理器
@mall_module.context_processor
def get_current_pos():
    return {"current_module": "商城", "current_module_url": url_for(".index")}
