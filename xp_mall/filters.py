# coding:utf-8

# 模板过滤函数，根据后台数据，返回对应文字
def create_filter(app):
    @app.template_filter()
    def get_order_status(status):
        status_list = {"0": "未支付", "1": "等待发货", "2": "等待收货", "3": "已收货", "4": "已取消"}
        return status_list[status]
