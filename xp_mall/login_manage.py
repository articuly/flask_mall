# coding:utf-8

from flask import render_template, redirect, request, url_for, flash, jsonify, Blueprint
from flask_login import login_user, current_user
from xp_mall.forms.member import LoginForm, RegisterForm
from xp_mall.models.member import Member
from xp_mall.utils import redirect_back
from xp_mall.extensions import db
from datetime import timedelta, datetime

AuthManage = Blueprint("auth", __name__)


# 用户登陆
@AuthManage.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('html'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        user = Member.query.filter_by(username=username).first()
        if user:
            if username == user.username and user.validate_password(password):
                login_user(user, remember, duration=timedelta(days=7))
                return redirect_back()
            else:
                flash('Invalid username or password.', 'warning')
        else:
            flash('No account.', 'warning')
    return render_template('member/auth/login.html', form=form)


# 用户注册
@AuthManage.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('html'))
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        username = form.username.data
        password = form.password.data
        user = Member(username=username, email=email, reg_date=datetime.now())
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return "success"
    elif form.errors:
        return jsonify(form.errors)
    return render_template('member/auth/register.html', form=form, next=request.args.get('next', ''))
