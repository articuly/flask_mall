# coding:utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField


# 订单搜索表单
class SearchForm(FlaskForm):
    status = SelectField("订单状态", choices=[(0, "所有订单"), (1, "已支付订单"), (2, "已发货订单"),
                                          (3, "已收货订单"), (4, "已取消")])
    keyword = StringField("订单号")
    order_type = SelectField("结果排序", choices=[(1, "根据订单时间升序排列"), (2, "根据订单时间降序排列")])
