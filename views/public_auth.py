from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import login_required, logout_user, current_user, login_user
from werkzeug.security import generate_password_hash
from calendar_config import db, app
from modules.auth_user import CalendarUsers

from forms.auth_form import LoginForm, Register

auth = Blueprint(name="auth", import_name=__name__)


@auth.route("/register/", methods=['GET', 'POST'])
def register():
    """注册"""
    form = Register()
    emsg = None
    try:
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            password2 = form.password2.data
            if password2 == password:
                new_user = CalendarUsers(username=username, password=generate_password_hash(password, method="plain"),
                                         email=form.email.data, mobile=form.mobile.data)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                # 使用蓝图后 url_for 就要用 蓝图名.url的方法名
                log_message = str({"rout_url": "auth.register", "result": "注册登录成功", "emsg": emsg,
                                   "username": username, "password": password, "password2": password2,
                                   "user_ip": request.remote_addr})
                app.logger.info(log_message)
                return render_template('calendar/index.html')
                # return redirect(url_for("calendar_pub_view.show_user"))
            else:
                emsg = "密码不一致"
                log_message = str({"rout_url": "auth.register", "result": "注册失败", "emsg": emsg,
                               "username": username, "password": password, "password2": password2,
                                   "user_ip": request.remote_addr})
                app.logger.info(log_message)
                return render_template("calendar/register.html", form=form, emsg=emsg)
    except Exception as e:
        emsg = str(e)
        log_message = str({"rout_url": "auth.register", "result": "注册异常", "emsg": emsg,
                           "username": username, "password": password, "password2": password2,
                           "user_ip": request.remote_addr})
        app.logger.error(log_message)
    return render_template("calendar/register.html", form=form, emsg=emsg)


@auth.route('/login/', methods=('GET', 'POST'))  # 登录
def login():
    """登录"""
    if current_user.is_authenticated:
        return redirect(url_for("calendar_pub_view.show_user"))
    form = LoginForm()  # 向模板传递表单参数
    emsg = None
    try:
        if request.method == "POST":
            if form.validate_on_submit():  # 是否点击提交
                user = CalendarUsers.query.filter(CalendarUsers.username == form.username.data).first()
                if user:
                    if user.validate_password(form.password.data):
                        login_user(user, remember=True)
                        log_message = str({"rout_url": "auth.login", "result": "登录成功", "emsg": emsg,
                                           "username": current_user.username, "user_ip": request.remote_addr})
                        app.logger.info(log_message)
                        return render_template('calendar/index.html')
                        # return redirect(url_for("calendar_pub_view.show_user"))
                    else:
                        emsg = "密码不正确"
                        log_message = str({"rout_url": "auth.login", "result": "登录失败", "emsg": emsg,
                                           "username": current_user.username, "password": form.password.data,
                                           "user_ip": request.remote_addr})
                        app.logger.info(log_message)
                        return render_template('calendar/login.html', form=form, emsg=emsg)
                else:
                    emsg = "用户未注册"
                    log_message = str({"rout_url": "auth.login", "result": "登录失败", "emsg": emsg,
                                       "username": form.username.data, "user_ip": request.remote_addr})
                    app.logger.info(log_message)
                    return render_template('calendar/login.html', form=form, emsg=emsg)
    except Exception as e:
        emsg = str(e)
        log_message = str({"rout_url": "auth.login", "result": "登录异常", "emsg": emsg,
                           "username": form.username.data, "password": form.password.data,
                           "user_ip": request.remote_addr})
        app.logger.error(log_message)
        return render_template('calendar/login.html', form=form, emsg=emsg)
    return render_template('calendar/login.html', form=form, emsg=emsg)


@auth.route('/logout/')
@login_required
def logout():
    """登出"""
    # current_user为CalendarUsers类的用户对象，可使用CalendarUsers类内的所有方法和变量
    now_user = current_user.username
    emsg = None
    try:
        logout_user()
        log_message = str({"rout_url": "auth.logout", "result": "注销成功", "emsg": emsg,
                           "username": now_user, "user_ip": request.remote_addr})
        app.logger.info(log_message)
    except Exception as e:
        emsg = str(e)
        log_message = str({"rout_url": "auth.logout", "result": "注销异常", "emsg": emsg,
                           "username": now_user, "user_ip": request.remote_addr})
        app.logger.error(log_message)
    finally:
        return redirect(url_for('auth.login'))
