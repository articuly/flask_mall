# coding:utf-8

from xp_mall.extensions import db, whooshee


# 商品类
@whooshee.register_model("goods_title", "detail")
class Goods(db.Model):
    goods_id = db.Column(db.Integer, primary_key=True)
    goods_title = db.Column(db.String(100))
    goods_subhead = db.Column(db.String(100))
    category_id = db.Column(db.Integer, db.ForeignKey('goods_category.id'))
    thumb = db.Column(db.String(100))
    main_pic = db.Column(db.String(500))
    price = db.Column(db.DECIMAL(12, 2))
    detail = db.Column(db.TEXT)
    create_time = db.Column(db.DateTime)
    is_recommend = db.Column(db.Integer)

    category = db.relationship('GoodsCategory')
