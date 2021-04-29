from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import login_required, current_user
from calendar_config import db, app

calendar_pub_view = Blueprint(name="calendar_pub_view", import_name=__name__)


@calendar_pub_view.route('/create_table/', methods=('GET', 'POST'))
def create_table():
    """初始化，创建所有模型里的表"""
    emsg = None
    try:
        db.create_all()
        emsg = "新建所有modules内所有表成功"
        log_message = str({"rout_url": "calendar_pub_view.create_table", "result": "创建表成功", "emsg": emsg,
                           "user_ip": request.remote_addr})
        app.logger.info(log_message)
    except Exception as e:
        emsg = str(e)
        log_message = str({"rout_url": "calendar_pub_view.create_table", "result": "创建表异常", "emsg": emsg,
                           "user_ip": request.remote_addr})
        app.logger.info(log_message)
    finally:
        return redirect(url_for("calendar_pub_view.root"))


@calendar_pub_view.route('/', methods=('GET', 'POST'))  # 首页
@login_required  # 装饰器，需要登录才能访问, 未登录时跳转到默认登录视图
def root():
    emsg = None
    log_message = str({"rout_url": "calendar_pub_view.root", "result": "/", "emsg": emsg,
                       "user_ip": request.remote_addr})
    app.logger.info(log_message)
    return render_template('calendar/index.html')














