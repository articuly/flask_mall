# coding:utf-8

from xp_mall.extensions import db


class Area(db.Model):
    place_id = db.Column(db.Integer, primary_key=True)
    place_name = db.Column(db.String(50))
    place_order = db.Column(db.Integer, default=0)
    parent_id = db.Column(db.Integer, db.ForeignKey('area.place_id'), default=None)

    up_place = db.relationship('Area', back_populates="sub_place", remote_side=[place_id])
    sub_place = db.relationship('Area', back_populates="up_place", cascade='all, delete-orphan',
                                order_by=place_order)
