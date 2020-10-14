# coding:utf-8
from flask import request, render_template, current_app, flash, url_for
from flask_login import current_user
from xp_mall.mall import mall_module
from xp_mall.models.category import GoodsCategory
from xp_mall.utils import redirect_back, redirect
from xp_mall.models.goods import Goods
from xp_mall.models.order import Cart
from ..utils import get_all_subcate, get_all_parent


# 商城首页
@mall_module.route('/<int:page>')
@mall_module.route('/', defaults={'page': 1})
def index(page):
    # 商品列表分页对象
    # page = request.args.get('page', 1, type=int)
    per_page = current_app.config['XPMALL_GOODS_PER_PAGE']
    res = Goods.query.order_by(Goods.create_time.desc()).paginate(page, per_page=per_page)
    goods_list = res.items
    pageList = res.iter_pages()
    # categories = GoodsCategory.query.order_by(GoodsCategory.id).first()

    # 已登陆用户，计算购物车图标的商品总数量与金额
    if current_user.user_id != 0:
        cart = Cart.query.filter_by(user_id=current_user.user_id).all()
        cart_amount, cart_total = 0, 0
        if cart:
            for item in cart:
                cart_amount = cart_amount + item.amount
                cart_total = cart_total + item.goods.price * item.amount
            print(cart_amount, cart_total)
            return render_template('mall/index.html', res=res, goods_list=goods_list, pageList=pageList,
                                   cart_amount=cart_amount, cart_total=cart_total)
        else:
            return render_template('mall/index.html', res=res, goods_list=goods_list, pageList=pageList,
                                   cart_amount=cart_amount, cart_total=cart_total)
    # 非登陆用户，则不传出购物车信息
    return render_template("mall/index.html", res=res, goods_list=goods_list, pageList=pageList)


# 商品搜索，未修改
@mall_module.route("/search")
def search():
    q = request.args.get('q', '')
    if q == '':
        flash('请输入搜索关键字')
        return redirect_back()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['XPMALL_GOODS_PER_PAGE']

    pagination = Goods.query.whooshee_search(q).paginate(page, per_page)
    goods = pagination.items
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['XPCMS_ARTICLE_PER_PAGE']
    pagination = Goods.query.filter(Goods.category_id.in_(sub_categories)).order_by(Goods.timestamp.desc()).paginate(
        page, per_page=per_page)
    goods = pagination.items
    return render_template("article/search.html", q=q, goods=goods, pagination=pagination, )


# 商品详情页
@mall_module.route('/detail/<int:category_id>/<int:goods_id>', methods=['GET', 'POST'])
def show_goods(category_id, goods_id):
    goods = Goods.query.get_or_404(goods_id)
    # 获取分类目录树
    category_tree = get_all_parent(goods.category_id)  #
    category_tree.sort(key=lambda x: x[1], reverse=False)
    categories = GoodsCategory.query.filter_by(id=category_tree[0][1]).order_by(GoodsCategory.order_id).first()
    # 已登陆用户，计算购物车图标的商品总数量与金额
    if current_user.user_id != 0:
        cart = Cart.query.filter_by(user_id=current_user.user_id).all()
        cart_amount, cart_total = 0, 0
        if cart:
            for item in cart:
                cart_amount = cart_amount + item.amount
                cart_total = cart_total + item.goods.price * item.amount
            print(cart_amount, cart_total)
            return render_template('mall/goods/detail.html', goods=goods, category=categories,
                                   category_tree=category_tree, cart_amount=cart_amount, cart_total=cart_total)
        else:
            return render_template('mall/goods/detail.html', goods=goods, category=categories,
                                   category_tree=category_tree, cart_amount=cart_amount, cart_total=cart_total)
    # 非登陆用户，则不传出购物车信息
    return render_template('mall/goods/detail.html', goods=goods, category=categories, category_tree=category_tree)


# 商品分类列表，未修改
@mall_module.route('/category/<int:category_id>/', methods=["GET"])
def category_lists(category_id):
    category_tree = get_all_parent(category_id)
    category_tree.sort(key=lambda x: x[1], reverse=False)
    categories = GoodsCategory.query.filter_by(id=category_tree[0][1]).order_by(GoodsCategory.order_id).first()
    sub_categories = get_all_subcate(category_id, [])
    return render_template('goods/lists.html', category=categories,
                           category_tree=category_tree)
