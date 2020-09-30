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
    form = UserAddressForm()
    if form.validate_on_submit():
        receiver = form.data['receiver']
        mobile = form.data['mobile']
        address = form.data['address']
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
            message = {'result': 'added'}
            # return jsonify(message)
            return redirect(url_for('member.address_list'))
    return render_template('member/address/new_address.html', form=form)


@member_module.route('/address_list', methods=['get', 'post'])
def address_list():
    page = request.args.get('page', 1)
    res = UserAddress.query.filter(UserAddress.user_id == current_user.user_id).order_by(
        UserAddress.id.desc()).paginate(int(page), current_app.config['XPMALL_MANAGE_GOODS_PER_PAGE'])
    addresses = res.items
    pageList = res.iter_pages()
    total = res.total
    pages = res.pages
    return render_template('member/address/address_list.html', addresses=addresses, pageList=pageList, total=total,
                           pages=pages)


@member_module.route('/delete_address/<int:address_id>', methods=['get', 'post'])
def delete_address(address_id):
    address = UserAddress.query.get(address_id)
    # 只能删除自己的地址
    if address.user_id == current_user.user_id:
        db.session.delete(address)
        db.session.commit()
    return redirect(url_for('member.address_list'))


@member_module.route('/edit_address/<int:address_id>', methods=['get', 'post'])
def edit_address(address_id):
    form = UserAddressForm()
    address = UserAddress.query.get(address_id)
    if not address:
        return redirect(url_for('member.address_list'))
    if form.validate_on_submit():
        # 只能修改自己的文章
        if address.user_id == current_user.user_id:
            address.receiver = form.data['receiver']
            address.mobile = form.data['mobile']
            address.address = form.data['address']
            try:
                db.session.add(address)
                db.session.commit()
            except Exception as e:
                print(e)
            else:
                return redirect(url_for('member.address_list'))
    elif form.errors:
        print(form.errors)
    else:
        form.receiver.data = address.receiver
        form.mobile.data = address.mobile
        form.address.data = address.address
    return render_template('member/address/edit_address.html', address=address, form=form)
