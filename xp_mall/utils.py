# coding:utf-8
try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

import os
from datetime import date, datetime
import uuid
import random
import time
from PIL import Image
from flask import current_app, jsonify, request, redirect, send_from_directory, url_for
from flask_ckeditor import upload_fail, upload_success
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from xp_mall.extensions import db
from xp_mall.models.category import GoodsCategory
from xp_mall.models.member import Member
from xp_mall.models.order import Order


def is_safe_url(target):
    '''
    检测安全网址
    :param target:
    :return:
    '''
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def allowed_file(filename):
    '''
    上传文件类型检测
    :param filename:
    :return:
    '''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config[
        'XPMALL_ALLOWED_IMAGE_EXTENSIONS']


def rename_image(old_filename):
    '''
    重命名上传文件
    :param old_filename:
    :return:
    '''
    ext = os.path.splitext(old_filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


def resize_image(image, filename, base_width, module):
    '''
    缩放图片
    :param image:
    :param filename:
    :param base_width:
    :param module:
    :return:
    '''
    base_size = current_app.config[module + '_PHOTO_SIZE'][base_width]
    filename, ext = os.path.splitext(filename)
    img = Image.open(image)
    filename += current_app.config[module + '_PHOTO_SUFFIX'][base_width] + ext
    upload_path = current_app.config[module + '_UPLOAD_PATH']
    if img.size[0] > base_size:
        w_percent = (base_size / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_size, h_size), Image.ANTIALIAS)
        img.save(os.path.join(upload_path, filename), optimize=True, quality=85)
    else:
        img.save(os.path.join(upload_path, filename), optimize=True, quality=85)
    return filename


def upload_image(module):
    '''
    图片上传
    :param module:
    :return:
    '''
    f = request.files.get('upload')
    if not allowed_file(f.filename):
        return upload_fail('Image only!')
    save_dir = date.today().strftime("%Y/%m/%d")
    new_filename = os.path.join(save_dir, rename_image(f.filename))
    upload_path = current_app.config[module + '_UPLOAD_PATH']
    try:
        f.save(os.path.join(upload_path, new_filename))
    except FileNotFoundError as e:
        os.makedirs(os.path.join(upload_path, save_dir))
        f.save(os.path.join(upload_path, new_filename))
    return new_filename, f


def upload_thumb(module):
    '''
    缩略图生成
    :param module:
    :return:
    '''
    if request.method == 'POST' and 'upload' in request.files:
        master_filename, f = upload_image(module)
        filename_s = resize_image(f, master_filename, 'small', module)
        filename_m = resize_image(f, master_filename, 'medium', module)
    return master_filename, filename_s, filename_m


def generate_token(user, operation, expire_in=None, **kwargs):
    '''
    生成token
    :param user:
    :param operation:
    :param expire_in:
    :param kwargs:
    :return:
    '''
    s = Serializer(current_app.config['SECRET_KEY'], expire_in)
    data = {'id': user.id, 'operation': operation}
    data.update(**kwargs)
    return s.dumps(data)


def validate_token(user, token, operation):
    '''
    验证token
    :param user:
    :param token:
    :param operation:
    :return:
    '''
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return False
    if operation != data.get('operation') or user.id != data.get('id'):
        return False
    if operation == Operations.CONFIRM:
        user.confirmed = True
    else:
        return False
    db.session.commit()
    return True


def redirect_back(default='index', **kwargs):
    '''
    页面跳转返回，如果参数含有next，跳转会next页面
    '''
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def get_all_parent(id):
    '''
    获得某个分类的所有父类
    '''
    category = db.session.query(GoodsCategory.parent_id, GoodsCategory.name, GoodsCategory.id).filter_by(
        id=id).order_by(GoodsCategory.id).first()
    if category.parent_id != None:
        return [(category.name, category.id)] + get_all_parent(category.parent_id)
    else:
        # print(category.name, category.id)
        return [(category.name, category.id)]


def get_all_subcate(id, all_cate_id=[]):
    '''
    获得某个分类的所有的子类
    :param id:
    :param all_cate_id:最后获得的分类列表
    :return:
    '''
    category = db.session.query(GoodsCategory).get(id)
    all_cate_id.append(id)
    if len(category.sub_cates) > 0:
        for sub_cate in category.sub_cates:
            get_all_subcate(sub_cate.id, all_cate_id)
    return set(all_cate_id)


def queryObjToDicts(obj, keys):
    '''
    将查询结果对象转换为列表类型
    :param obj:
    :param keys:
    :return:
    '''
    lists = [{key: getattr(item, key) for key in keys} for item in obj]
    return lists


def get_pay_obj(payment):
    '''
    获得支付接口对象
    :param payment:
    :return:
    '''
    return current_app.extensions[payment]


def add_random_member(n):
    '''
    添加N个随机用户
    :param n:
    :return:
    '''
    words = list('abcdefghijklmnopqrstuvwxyz')
    emails = ['@qq.com', '@gmail.com', '@126.com', '@163.com', '@hotmail.com', '@sohu.com', '@sogou.com']
    stime = datetime.strptime('2020-09-28', "%Y-%m-%d")
    etime = datetime.strptime('2020-10-31', "%Y-%m-%d")
    for i in range(n):
        random.shuffle(words)
        username = ''.join(words[:6])
        reg_sex = str(random.randint(0, 2))
        email = username + random.choice(emails)
        # 随机注册时间
        reg_date = random.random() * (etime - stime) + stime
        member = Member(
            username=username,
            email=email,
            reg_sex=reg_sex,
            reg_date=reg_date,
        )
        member.set_password('123654')
        db.session.add(member)
    db.session.commit()


def add_random_order(n):
    '''
    添加N张随机订单
    :param n:
    :return:
    '''
    stime = datetime.strptime('2020-09-28', "%Y-%m-%d")
    etime = datetime.strptime('2020-10-31', "%Y-%m-%d")
    subject = '测试商城订单'
    for i in range(n):
        total_price = random.randint(1000, 10000)
        status = random.choices(['0', '1', '2', '3', '4'], weights=(0.1, 0.3, 0.2, 0.3, 0.1), k=1)[0]
        buyer = str(random.randint(100, 1000))
        payment = random.choices(['wxpay', 'alipay'], weights=[0.2, 0.8], k=1)[0]
        createTime = random.random() * (etime - stime) + stime
        order_no = str(time.strftime('%Y%m%d%H%M%S', time.localtime(createTime.timestamp()))) + str(
            time.time()).replace('.', '')[-7:]
        order = Order(
            order_no=order_no,
            subject=subject,
            total_price=total_price,
            status=status,
            buyer=buyer,
            payment=payment,
            createTime=createTime
        )
        db.session.add(order)
    db.session.commit()
