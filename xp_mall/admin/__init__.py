# coding:utf-8

from flask import render_template, redirect, url_for, Blueprint
from flask_login import current_user, login_required
from xp_mall.models.order import Cart
import random
import pandas as pd
from pyecharts.charts import Bar, Pie, Line, Page
from pyecharts import options as opts
from sqlalchemy import create_engine
import datetime
from datetime import timedelta

admin_module = Blueprint('admin', __name__)

from xp_mall.admin.goods import *
from xp_mall.admin.category import *
from xp_mall.admin.upload import *
from xp_mall.admin.orders import *
from xp_mall.admin.area import *

# from xp_mall.forms.settings import SettingForm

# 读取数据库
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/mymall')
member = pd.read_sql_query('select * from `member`;', engine)
order = pd.read_sql_query('select * from `order`;', engine)
# 替换性别数值
member['reg_sex'] = member['reg_sex'].replace({'0': '保密', '1': '男', '2': '女'})
# 今天日期，与七天前日期
t = datetime.datetime.now()
td = t.date()
d7_before = t - timedelta(days=7)
# 今天的用户数据处理
today_member = member[member['reg_date'].dt.date == td]
reg_sex_count = today_member.groupby('reg_sex')['reg_sex'].count().to_dict()
# 最近七天的用户数据处理
d7_member = member[(member['reg_date'].dt.date >= d7_before.date()) & (member['reg_date'].dt.date < td)]
d7_reg_count = d7_member['reg_date'].dt.date.value_counts().sort_index().to_dict()
d7_reg_count_dict = {datetime.datetime.strftime(k, '%F'): v for k, v in d7_reg_count.items()}
# 今天的订单数据处理
today_order = order[order['createTime'].dt.date == td]
today_order_total = today_order[today_order['status'] == '3']['total_price'].sum()
status_list = {"0": "未支付", "1": "等待发货", "2": "等待收货", "3": "已收货", "4": "已取消"}
order_status_total = {}
for k, v in status_list.items():
    total = today_order[today_order['status'] == k]['total_price'].sum()
    order_status_total.update({v: total})
# 最近七天的用户数据处理
d7_order = order[(order['createTime'].dt.date >= d7_before.date()) & (order['createTime'].dt.date < td)]
d7_order_finish = d7_order[d7_order['status'] == '3']  # 只统计交易完成的订单
d7_order_finish_count = d7_order_finish['createTime'].dt.date.value_counts().sort_index().to_dict()
d7_order_finish_dict = {datetime.datetime.strftime(k, '%F'): v for k, v in d7_order_finish_count.items()}
d7_order_finish['createTime'] = d7_order_finish['createTime'].dt.date
d7_order_finish_total = d7_order_finish.groupby('createTime')['total_price'].sum().sort_index().to_dict()
d7_order_finish_total_dict = {datetime.datetime.strftime(k, '%F'): v for k, v in d7_order_finish_total.items()}


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
    return render_template("admin/admin_index.html", today_member_num=today_member.shape[0],
                           today_order_num=today_order.shape[0], today_order_total=today_order_total)


# 生成用户信息图表
@admin_module.route("/member_chart")
def member_chart():
    # 今日注册用户性别占比
    c = (
        Pie()
            .add("", list(reg_sex_count.items()))
            .set_global_opts(title_opts=opts.TitleOpts(title="今日注册用户性别占比"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}")))
    return c.dump_options_with_quotes()


@admin_module.route("/member7_chart")
def member7_chart():
    # 最近七天注册人数
    line1 = Line()
    line1.add_xaxis(list(d7_reg_count_dict.keys()))
    line1.add_yaxis("人数", list(d7_reg_count_dict.values()), linestyle_opts=opts.LineStyleOpts(width=5))
    line1.set_global_opts(title_opts=opts.TitleOpts(title="最近七天注册人数"))
    return line1.dump_options_with_quotes()


# 生成订单信息图表
@admin_module.route("/order_chart")
def order_chart():
    # 今日各状态订单总金额
    pie2 = Pie()
    pie2.add("", list(order_status_total.items()))
    pie2.set_global_opts(title_opts=opts.TitleOpts(title="今日各状态订单总金额"))
    pie2.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    return pie2.dump_options_with_quotes()


@admin_module.route("/order7_chart")
def order7_chart():
    # 最近七天订单确认成交数量
    line2 = Line()
    line2.add_xaxis(list(d7_order_finish_dict.keys()))
    line2.add_yaxis("数量", list(d7_order_finish_dict.values()), itemstyle_opts=opts.ItemStyleOpts(color='blue'),
                    linestyle_opts=opts.LineStyleOpts(width=5))
    line2.set_global_opts(title_opts=opts.TitleOpts(title="最近七天订单确认成交数量"))
    return line2.dump_options_with_quotes()


@admin_module.route("/order7_total_chart")
def order7_total_chart():
    # 最近七天订单确认成交金额
    bar = Bar()
    bar.add_xaxis(list(d7_order_finish_total_dict.keys()))
    bar.add_yaxis("金额", list(d7_order_finish_total_dict.values()), itemstyle_opts=opts.ItemStyleOpts(color='orange'))
    bar.set_global_opts(title_opts=opts.TitleOpts(title="最近七天订单确认成交金额"))
    return bar.dump_options_with_quotes()


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
