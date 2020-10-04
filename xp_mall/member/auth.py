# coding:utf-8

from flask import request, render_template, flash, redirect, url_for
from flask_login import logout_user
from xp_mall.utils import redirect_back
from xp_mall.member import member_module


# 用户登出
@member_module.route('/logout')
def logout():
    logout_user()
    flash('顺利登出', 'info')
    return redirect_back()
