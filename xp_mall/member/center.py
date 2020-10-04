# -*- coding=utf-8 -*-

from flask import Flask, request, render_template, url_for, \
    jsonify, current_app

from flask_login import current_user

from xp_mall.models.member import Member
from xp_mall.models.goods import Goods
from xp_mall.models.order import Order, OrderGoods, Cart, Logistics
from xp_mall.extensions import db
from xp_mall.member import member_module
from xp_mall.forms.order import SearchForm
from xp_mall.forms.member import EditInfoForm


@member_module.route("/")
def center_index():
    return render_template("member/member_index.html")


@member_module.route("/cart")
def cart_list():
    cart_list = Cart.query.filter_by(user_id=current_user.user_id).all()
    return render_template("member/cart/cart_list.html", cart_list=cart_list)


# 修改用户信息
@member_module.route("/profile", methods=['get', 'post'])
def profile():
    print(current_user.is_admin)
    print(type(current_user.is_admin))
    message = None
    form = EditInfoForm()
    user = Member.query.filter_by(user_id=current_user.user_id).one()
    if form.validate_on_submit():
        user.email = form.data['email']
        user.sex = form.data['sex']
        user.mobile = form.data['mobile']
        password = form.data['password']
        if user.validate_password(password):
            try:
                db.session.commit()
                message = '修改成功'
            except Exception as e:
                print(str(e))
                message = '后台发生错误'
        else:
            message = '用户名与密码不匹配'
    elif form.errors:
        print(form.errors)
        message = '表单发生错误'
    else:
        form.email.data = user.email
        form.sex.data = user.reg_sex
        form.mobile.data = user.mobile
    return render_template("member/info/info_edit.html", message=message, user=user, form=form)


@member_module.route('/myorders', defaults={'page': 1})
@member_module.route('/myorders/<int:page>', methods=['GET'])
def manage_orders(page):
    form = SearchForm()
    order_query = Order.query.filter_by(buyer=current_user.user_id)
    status = request.args.get("status", None)
    if status:
        form.status = status
        order_query = order_query.filter_by(status=status)

    keyword = request.args.get("keyword", None)
    if keyword:
        form.keyword.data = keyword
        order_query = order_query.whooshee_search(keyword)

    if request.args.get("order_type"):
        order_type = request.args.get("order_type")
        form.order_type.data = order_type
        if order_type == "1":
            order_type = Order.create_time.asc()
        elif order_type == "2":
            order_type = Order.create_time.desc()
        elif order_type == "3":
            order_type = Order.price.asc()
        else:
            order_type = Order.create_time.desc()
        order_query = order_query.order_by(order_type)
    # print(order_query)
    pagination = order_query.paginate(
        page, current_app.config['XPMALL_MANAGE_GOODS_PER_PAGE'])
    condition = request.query_string.decode()

    # 查询订单物流信息
    q = order_query.filter(Order.status == '2')
    user_order = [item.id for item in q.all()]
    if user_order:
        print(user_order)
        sent_order = Logistics.query.filter(Logistics.order_id.in_(user_order))
        # for row in sended_order:
        #     print(row.logis_company, row.logis_number)
        return render_template('member/order/order_list.html', page=page,
                               pagination=pagination, form=form,
                               condition=condition, sent_order=sent_order)
    return render_template('member/order/order_list.html', page=page,
                           pagination=pagination, form=form,
                           condition=condition)


@member_module.route('/order/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    # 用户只能取消自己的订单
    if int(order.buyer) == current_user.user_id:
        print(order.buyer)
        order.status = 4
        db.session.commit()
        return "ok"
    else:
        return 'fail'


@member_module.route('/order/receive_goods/<int:order_id>', methods=['post'])
def receive_goods(order_id):
    order = Order.query.get_or_404(order_id)
    logis = Logistics.query.filter(Logistics.order_id == order_id).one()
    # 用户只能确认自己的订单
    if int(order.buyer) == current_user.user_id:
        order.status = 3
        logis.status = 3
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            return 'fail'
        else:
            return 'ok'
