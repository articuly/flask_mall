# coding:utf-8
import time, math, datetime

from flask import current_app, render_template, redirect, \
    request, jsonify, url_for
from flask_login import current_user, login_required
from xp_mall.extensions import db, csrf
from xp_mall.member import member_module
from xp_mall.models.member import UserAddress
from xp_mall.forms.member import UserAddressForm



@member_module.route('/new_address', methods=['get', 'post'])
def new_address():
    print(current_user.user_id)
    form=UserAddressForm()
    if form.validate_on_submit():
        receiver=form.data['receiver']
        mobile=form.data['mobile']
        address=form.data['address']
        print(receiver, mobile, address)
        user_address = UserAddress(
            receiver=receiver,
            mobile=mobile,
            address=address,
            user_id=current_user.user_id,
        )
        try:
            db.session.add(user_address)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        else:
            message={'result':'added'}
            # return jsonify(message)
            return render_template('member/member_index.html')
    return render_template('member/address/new_address.html', form=form)










