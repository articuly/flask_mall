# coding:utf-8

from flask import Blueprint, redirect, url_for

member_module = Blueprint('member', __name__)

from xp_mall.member.center import *
from xp_mall.member.cart import *
from xp_mall.member.buy import *
from xp_mall.member.auth import *
from xp_mall.member.address import *
from flask_login import login_required, current_user


# 检测用户是否登陆
@member_module.before_request
@login_required
def is_login():
    # print(current_user.username)
    pass


@member_module.context_processor
def getCart():
    '''
    计算购物车信息
    :return: 购物车商品数量总数，总金额
    '''
    cart = Cart.query.filter_by(user_id=current_user.user_id).all()
    cart_amount, cart_total = 0, 0
    if cart:
        for item in cart:
            cart_amount = cart_amount + item.amount
            cart_total = cart_total + item.goods.price * item.amount
        print(cart_amount, cart_total)
        return {'cart_amount': cart_amount, 'cart_total': cart_total}
    else:
        return {'cart_amount': cart_amount, 'cart_total': cart_total}
