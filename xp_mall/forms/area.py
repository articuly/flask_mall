# coding:utf-8

from flask import g
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError
from xp_mall.models.area import Area


# 地区表单
class AreaForm(FlaskForm):
    parent_id = HiddenField('Parent')
    place_name = StringField('地方名', validators=[DataRequired(), Length(1, 50)])
    place_order = IntegerField('显示顺序')
    submit = SubmitField()

    # 添加与修改地方名时，要检测是否重复
    def validate_name(self, field):
        if g.get("place_id") is None:
            if Area.query.filter_by(name=field.data).first():
                raise ValidationError('地区名称重复.')
        else:
            exits_area = Area.query.filter_by(name=field.data).first()
            if exits_area and exits_area.place_id != g.get("place_id"):
                raise ValidationError('地区名称重复')
