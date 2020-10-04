# coding:utf-8

from flask_wtf import FlaskForm
from wtforms import IntegerField


# 购买数量表单
class OrderForm(FlaskForm):
    amount = IntegerField('购买数量')
