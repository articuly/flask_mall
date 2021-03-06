# coding:utf-8

from flask import g
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, FloatField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError
from xp_mall.models.category import GoodsCategory


# 商品信息表单
class GoodsForm(FlaskForm):
    title = StringField('商品标题', validators=[DataRequired(), Length(1, 60)])
    subhead = StringField('商品副标题')
    category = HiddenField('Category')
    thumb = HiddenField('商品首图')
    main_pic = HiddenField('商品主图')
    body = CKEditorField('商品描述', validators=[DataRequired()])
    price = FloatField('商品价格', validators=[DataRequired()])


# 商品分类表单
class CategoryForm(FlaskForm):
    parent_id = HiddenField('Parent')
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    order_id = IntegerField('OrderNo')
    submit = SubmitField()

    # 添加与修改分类时，要检测是否分类名是否重复
    def validate_name(self, field):
        if g.get("category_id") is None:
            if GoodsCategory.query.filter_by(name=field.data).first():
                raise ValidationError('分类名称重复.')
        else:
            exits_cate = GoodsCategory.query.filter_by(name=field.data).first()
            if exits_cate and exits_cate.id != g.get("category_id"):
                raise ValidationError('分类名称重复')


# 商品搜索表单
class SearchForm(FlaskForm):
    category_id = HiddenField("分类id")
    keyword = StringField("搜索关键词")
    order_type = SelectField("结果排序", choices=[(1, "根据发布时间升序排列"), (2, "根据发布时间降序排列"),
                                              (3, "根据商品价格升序排列"), (4, "根据商品价格降序排列"), ])
