# coding:utf-8

from xp_mall.extensions import db


# todo:在物流信息加入地区地址
class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(50))
    order_id = db.Column(db.Integer, default=0)
    parent_id = db.Column(db.Integer, db.ForeignKey('area.id'), default=None)

    parent = db.relationship('Area', back_populates="sub_cates", remote_side=[id])
    sub_cates = db.relationship('Area', back_populates="parent", cascade='all, delete-orphan',
                                order_by=order_id)
