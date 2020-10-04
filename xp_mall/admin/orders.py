# coding:utf-8

from flask import render_template, request, current_app, redirect, url_for, jsonify
from xp_mall.extensions import db
from xp_mall.admin import admin_module
from xp_mall.models.goods import Goods
from xp_mall.models.order import Order, Logistics
from xp_mall.forms.order import SearchForm


# 订单管理
@admin_module.route('/manage/orders', defaults={'page': 1})
@admin_module.route('/manage/orders/<int:page>', methods=['GET'])
def manage_orders(page):
    form = SearchForm()
    order_query = Order.query
    status = request.args.get("status", None)
    # 各种搜索条件
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
            order_type = Order.createTime.asc()
        elif order_type == "2":
            order_type = Order.createTime.desc()
        elif order_type == "3":
            order_type = Order.price.asc()
        else:
            order_type = Order.createTime.desc()
        order_query = order_query.order_by(order_type)

    condition = request.query_string.decode()
    # print('condition:\n', condition)
    # 分页对象
    pagination = order_query.paginate(page, current_app.config['XPMALL_MANAGE_GOODS_PER_PAGE'])

    # 查询已发货订单物流信息
    sent_order = Logistics.query.filter(Logistics.status == '2').all()
    if sent_order:
        return render_template('admin/order/order_list.html', page=page, pagination=pagination, form=form,
                               condition=condition, sent_order=sent_order)

    return render_template('admin/order/order_list.html', page=page, pagination=pagination, form=form,
                           condition=condition)


# 编辑订单
@admin_module.route('/orders/<int:order_id>/edit', methods=['GET', 'POST'])
def edit_order(order_id):
    pass
    # form = GoodsForm()
    # goods = Goods.query.get_or_404(goods_id)
    # if form.validate_on_submit():
    #     goods.goods_title = form.title.data
    #     goods.detail  = form.body.data
    #     goods.thumb = form.thumb.data
    #     goods.main_pic = form.main_pic.data
    #     goods.category_id = form.category.data
    #     goods.price = form.price.data
    #     db.session.commit()
    # elif form.errors:
    #     print(form.errors)
    # form.title.data = goods.goods_title
    # form.body.data = goods.detail
    # thumbs = goods.main_pic
    # form.category.data = goods.category_id
    # form.price.data = goods.price
    # current_cate = goods.category.name
    # return render_template('admin/goods/goods_edit.html',
    #                        form=form, thumbs=thumbs,
    #                        current_cate=current_cate)


# 删除订单
@admin_module.route('/order/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = 4
    db.session.commit()
    return "ok"


# 发货管理
@admin_module.route('/order/logis_edit/<int:order_id>', methods=['post'])
def logis_edit(order_id):
    # print('logis', order_id)
    order = Order.query.get_or_404(order_id)
    logistics = Logistics.query.filter(Logistics.order_id == order_id).one()
    if request.method == 'POST':
        logis_company = request.form.get('logis_company')
        logis_number = request.form.get('logis_number')
        # print(logis_company, logis_number)
        # 改变订单状态，写入物流信息
        logistics.logis_company = logis_company
        logistics.logis_number = logis_number
        logistics.status = 2
        order.status = 2
        try:
            db.session.add(order)
            db.session.add(logistics)
            db.session.commit()
        except Exception as e:
            print(e)
        else:
            return jsonify({'result': 'saved'})
