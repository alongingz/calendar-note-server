from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """登录表单类"""
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])


class Register(FlaskForm):
    """注册表单类"""
    username = StringField(label="用户名", validators=[DataRequired()])
    password = StringField(label="密码", validators=[DataRequired()])
    password2 = StringField(label="密码确认", validators=[DataRequired()])
    email = StringField(label="邮箱", validators=[DataRequired()])
    mobile = StringField(label="手机号", validators=[DataRequired()])
