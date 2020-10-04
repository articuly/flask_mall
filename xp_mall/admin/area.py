# coding:utf-8

from flask import render_template, g, request, jsonify, current_app, redirect, flash, url_for
from flask_login import login_required
from xp_mall.admin import admin_module
from xp_mall.extensions import db
from xp_mall.forms.area import AreaForm
from xp_mall.models.area import Area


# Area地区管理
@admin_module.route('/area/manage/', defaults={"parent_id": 0}, methods=["GET"])
@admin_module.route('/area/manage/<int:parent_id>', methods=["GET"])
@login_required
def manage_area(parent_id):
    parent_id = parent_id if parent_id else None  # 默认为0，也为空值
    areas = Area.query.filter_by(parent_id=parent_id).order_by(Area.place_id).all()
    return render_template('admin/area/area_list.html', areas=areas)


# 增加地区
@admin_module.route('/area/new', methods=['GET', 'POST'])
@login_required
def new_area():
    form = AreaForm()
    if form.validate_on_submit():
        # 第一层级目录的父级为""
        # 使用0会发生约束完整性问题
        parent_id = form.parent_id.data if int(form.parent_id.data) else None
        place_name = form.place_name.data
        place_order = form.place_order.data
        area = Area(place_name=place_name, parent_id=parent_id, place_order=place_order)
        db.session.add(area)
        db.session.commit()
        # flash('Area created.', 'success')
        # return redirect(url_for('.manage_area'))
        return str(area.place_id)
    elif form.errors:
        return jsonify(form.errors)
    return render_template('admin/area/area_add.html', form=form)


# 编辑地区
@admin_module.route('/area/<int:place_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_area(place_id):
    message = None
    form = AreaForm()
    area = Area.query.get_or_404(place_id)
    g.place_id = area.place_id
    g.place_name = area.place_name
    print(area, g.place_id, g.place_name)
    if form.validate_on_submit():
        try:
            area.place_name = form.place_name.data
            area.parent_id = form.parent_id.data
            area.place_order = form.place_order.data
            db.session.commit()
        except Exception as e:
            print(e)
            current_app.logger.debug(e)
            message = e
        else:
            return redirect(url_for("admin.manage_area"))
    else:
        print(form.errors)
        current_app.logger.error("表单数据验证错误")
        message = str(form.errors)

    form.place_name.data = area.place_name
    form.parent_id.data = area.parent_id
    form.place_order.data = area.place_order
    return render_template('admin/area/area_edit.html', form=form, message=message)


# 删除地区
@admin_module.route('/area/delete', methods=['POST'])
@login_required
def delete_area():
    place_id = int(request.form['place_id'])
    area = Area.query.get_or_404(place_id)
    print(place_id, area)
    try:
        db.session.delete(area)
        db.session.commit()
    except Exception as e:
        return "fail"
    return "ok"


# 地区管理，传出所有级别菜单
@admin_module.route('/area', methods=['get'])
@login_required
def get_area():
    parent_id = request.args.get("parent_id", 0, type=int)
    parent_id = parent_id if parent_id else None
    sub_place = Area.query.filter_by(parent_id=parent_id).all()
    place_dicts = [(place.place_name, place.place_id) for place in sub_place]
    print(place_dicts)
    return jsonify(place_dicts)
