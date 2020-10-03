# -*- coding: utf-8 -*-
from flask import request, g
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField, \
    BooleanField, PasswordField, IntegerField, HiddenField, RadioField, widgets, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, Optional, URL, Regexp, EqualTo
from flask_login import current_user
from xp_mall.models.category import GoodsCategory
from xp_mall.models.member import Member


# from xp_cms.settings import Operations
# from xp_cms.utils import generate_token


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('一周内无需重新登陆')
    submit = SubmitField('立即登陆')


class RegisterForm(FlaskForm):
    username = StringField('用户名',
                           validators=[DataRequired(), Length(1, 20), Regexp('^[a-zA-Z0-9]*$', message='字母与数字组成')])
    email = StringField("电子邮箱", validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 30), EqualTo('password2')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    Submit = SubmitField()

    def validate_email(self, field):
        if Member.query.filter_by(email=field.data).first():
            raise ValidationError("The email is already in use.")

    def validate_username(self, field):
        if Member.query.filter_by(username=field.data).first():
            raise ValidationError("The username is already in use")


class BindForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField('Bind')


class ForgetPasswordForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    submit = SubmitField('提交')


class ResetPasswordForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 30), EqualTo('password2')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('提交')


class AddressForm(FlaskForm):
    receiver = StringField('收件人', validators=[DataRequired()])
    mobile = StringField("电话", validators=[DataRequired()])
    address = StringField("详细地址", validators=[DataRequired()])
    payment = HiddenField("支付方式", validators=[DataRequired()])


class UserAddressForm(FlaskForm):
    receiver = StringField('收件人', validators=[DataRequired()])
    mobile = StringField("电话", validators=[DataRequired()])
    address = StringField("详细地址", validators=[DataRequired()])


# 定义多选框的类
class CheckBoxField(SelectMultipleField):
    widget = widgets.TableWidget(with_table_tag=False)
    # widget = widgets.ListWidget()
    option_widget = widgets.CheckboxInput()


# 修改用户信息
class EditInfoForm(FlaskForm):
    email = StringField("电子邮箱：", validators=[DataRequired(), Length(1, 64), Email()])
    sex = RadioField('性别：', validators=[DataRequired(), ], render_kw={'class': 'd-flex'},
                     choices=[('0', '保密'), ('1', '男'), ('2', '女')])
    mobile = StringField("电话：", validators=[DataRequired(), Length(6, 20)])
    password = PasswordField('验证密码：',
                             validators=[DataRequired(message='必须提供密码'), Length(6, 20, message='密码长度在6-20位之间')],
                             render_kw={'placeholder': "请输入自己的密码"})

    def validate_email(self, field):
        if field.data != current_user.email:
            if Member.query.filter_by(email=field.data).first():
                raise ValidationError("The email is already in use.")
