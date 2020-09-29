# coding:utf-8

from flask import request, g
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, \
    IntegerField, FloatField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError
from xp_mall.models.area import Area


class AreaForm(FlaskForm):
    parent_id = HiddenField('Parent')
    place_name = StringField('地方名', validators=[DataRequired(), Length(1, 50)])
    place_order = IntegerField('显示顺序')
    submit = SubmitField()

    def validate_name(self, field):
        '''
        添加与修改地方名时，要检测是否重复
        :param field:
        :return:
        '''
        if g.get("place_id") is None:
            if Area.query.filter_by(name=field.data).first():
                raise ValidationError('分类名称重复.')
        else:
            exits_area = Area.query.filter_by(name=field.data).first()
            if exits_area and exits_area.place_id != g.get("place_id"):
                raise ValidationError('分类名称重复')
