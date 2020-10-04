# coding:utf-8

from xp_mall.extensions import db, whooshee


# 订单类
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(50))
    subject = db.Column(db.String(100))
    total_price = db.Column(db.DECIMAL(12, 2))
    status = db.Column(db.String(10))
    seller = db.Column(db.String(50))
    buyer = db.Column(db.String(50))
    createTime = db.Column(db.DATETIME)
    payment = db.Column(db.String(30))
    paytime = db.Column(db.DATETIME)

    goods = db.relationship('OrderGoods', back_populates='order', cascade='all, delete-orphan')
    logistics = db.relationship('Logistics', back_populates='order', cascade='all, delete-orphan')


# 订单商品类，两表的多对多关系要通过中间表连接
class OrderGoods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goods_id = db.Column(db.Integer, db.ForeignKey('goods.goods_id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    price = db.Column(db.DECIMAL(12, 2))
    order_price = db.Column(db.DECIMAL(12, 2))
    order_active = db.Column(db.String(255), default=None)
    amount = db.Column(db.Integer)
    discount = db.Column(db.DECIMAL(12, 2))

    order = db.relationship('Order', back_populates='goods')
    goods = db.relationship('Goods')


# 购物车类
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goods_id = db.Column(db.Integer, db.ForeignKey('goods.goods_id'))
    amount = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('member.user_id'))

    user = db.relationship('Member')
    goods = db.relationship('Goods')


# 物流信息类
class Logistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    status = db.Column(db.String(10))
    receiver = db.Column(db.String(20))
    mobile = db.Column(db.String(30))
    address = db.Column(db.String(100))
    logis_company = db.Column(db.String(50))
    logis_number = db.Column(db.String(20))

    order = db.relationship('Order')
