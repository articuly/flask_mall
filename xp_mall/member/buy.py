# coding:utf-8

import time, datetime
from flask import render_template, redirect, jsonify, url_for
from flask_login import current_user, login_required
from xp_mall.extensions import db, csrf
from xp_mall.member import member_module
from xp_mall.member.cart import empty
from xp_mall.forms.member import AddressForm
from xp_mall.models.order import Order, OrderGoods, Cart, Logistics
from xp_mall.models.member import UserAddress
from xp_mall.utils import get_pay_obj


# 订单创建
@member_module.route('/create_order', methods=['get', 'post'])
def create_order():
    # 获取用户所有地址
    addresses = UserAddress.query.filter(UserAddress.user_id == current_user.user_id).order_by(
        UserAddress.id.desc()).all()
    # 获取购物车商品
    cart_list = Cart.query.filter_by(user_id=current_user.user_id).all()
    total_price = get_total_price(cart_list)
    print('total_price:', total_price)
    form = AddressForm()
    if form.validate_on_submit() and cart_list:
        order = Order(
            order_no=get_order_no(),
            subject="测试商城订单",
            total_price=total_price,
            status='0',
            buyer=current_user.user_id,
            payment=form.payment.data,
            createTime=datetime.datetime.now()
        )
        logistics = Logistics(
            receiver=form.receiver.data,
            mobile=form.mobile.data,
            address=form.address.data,
            status='0',
        )
        # 记录订单商品信息，商品价格是变动的，需要记录下单时价格，以备核对
        [order.goods.append(OrderGoods(**{
            "goods_id": cart.goods.goods_id,
            "price": cart.goods.price,
            "order_price": cart.goods.price,
            "order_active": "",
            "amount": cart.amount,
            "discount": 100
        })) for cart in cart_list]
        order.logistics.append(logistics)

        try:
            empty()
            db.session.add(order)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        else:
            # 跳转到订单结算页面
            return redirect(url_for("member.pay_order", order_no=order.order_no))
    return render_template('member/order/buy.html', addresses=addresses, form=form, cart_list=cart_list,
                           total_price=total_price)


# 订单结算
@member_module.route('/pay_order/<order_no>', methods=['GET', 'POST'])
def pay_order(order_no):
    # 未支付订单进入结算
    order = Order.query.filter_by(order_no=order_no, status='0', buyer=current_user.user_id).first()
    if not order:
        return redirect(url_for('.index'))
    elif order.status == '1':
        return redirect(url_for('.index'))
    payment = order.payment
    pay = get_pay_obj(order.payment)
    # 根据支付方式，创建支付订单
    res = pay.pay_order(order)  # res为url
    if payment == "alipay":
        # 支付宝支付方式生成一个url地址
        return redirect(res)
    else:
        # 微信支付方式，获得一个包含url及其他信息数据
        # 根据返回的url生成二维码，扫码支付
        if res[0]:
            return render_template("member/order/buy_wxqrcode.html", out_trade_no=order.order_no,
                                   code_url=res[1]['code_url'])
        else:
            return jsonify(success=False, message="支付失败，您并没有任何损失，请联系网站管理员")


@member_module.route("/pay/status/<string:out_trade_no>", methods=['GET'])
def get_order_status(out_trade_no):
    '''
    微信支付是否完成接口，如果完成，那么二维码支付页面跳转到订单支付完成页面
    '''
    order = Order.query.filter_by(order_no=out_trade_no, buyer=current_user.user_id).first()
    if order.status == "1":
        return jsonify(success='success')
    else:
        return jsonify(success="wait")


def get_order_no():
    '''
    订单编号生成
    '''
    order_no = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))) + str(time.time()).replace('.', '')[-7:]
    return order_no


def get_total_price(cart_list):
    '''
    订单支付总价计算
    如果商城拥有活动，打折等功能，需要根据这些功能计算折扣价
    '''
    total_price = 0
    for cart in cart_list:
        total_price += cart.amount * cart.goods.price
    # 折扣价，活动价
    return total_price
