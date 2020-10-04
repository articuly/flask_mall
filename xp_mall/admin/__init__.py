# coding:utf-8

from flask import render_template, redirect, url_for, Blueprint
from flask_login import current_user, login_required
from xp_mall.models.order import Cart

admin_module = Blueprint('admin', __name__)

from xp_mall.admin.goods import *
from xp_mall.admin.category import *
from xp_mall.admin.upload import *
from xp_mall.admin.orders import *
from xp_mall.admin.area import *
# from xp_mall.forms.settings import SettingForm


# 检测管理员账户
@admin_module.before_request
@login_required
def is_admin():
    if not current_user.is_admin:
        return redirect(url_for("login"))


# 管理员首页
@admin_module.route('/', methods=['GET'])
@login_required
def index():
    return render_template("admin/admin_index.html")


@admin_module.context_processor
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

# @admin_module.route('/settings', methods=['GET', 'POST'])
# @login_required
# def settings():
#     form = SettingForm()
#     if form.validate_on_submit():
#         current_user.name = form.name.data
#         current_user.blog_title = form.blog_title.data
#         current_user.blog_sub_title = form.blog_sub_title.data
#         current_user.about = form.about.data
#         db.session.commit()
#         flash('Setting updated.', 'success')
#         return redirect(url_for('blog.index'))
#     form.name.data = current_user.name
#     form.blog_title.data = current_user.blog_title
#     form.blog_sub_title.data = current_user.blog_sub_title
#     form.about.data = current_user.about
#     return render_template('admin/settings.html', form=form)
