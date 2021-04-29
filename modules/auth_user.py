from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from calendar_config import db, login_manager


class CalendarUsers(db.Model, UserMixin):
    """用户数据库模型"""
    user_id = db.Column(db.Integer, autoincrement=True, unique=True, primary_key=True, comment="user_id")
    username = db.Column(db.String(length=255), unique=True, nullable=True, comment="用户名")
    password = db.Column(db.String(length=255), nullable=True, comment="密码")
    email = db.Column(db.String(length=255), comment="邮箱")
    mobile = db.Column(db.String(length=255), comment="手机号")
    group = db.Column(db.Integer, default=2,
                      comment="权限组。1: admin,管理员权限-查看、新增、修改-所有用户; 2: 公共的查看权限，本人的所有权限；"
                              "3：公共的查看、新增权限，本人的所有权限； 4、公共的查看、新增、修改权限-本人的所有权限；")

    def __init__(self, username, password, email="", mobile=0, group=2):
        self.username = username
        self.password = password
        self.email = email
        self.mobile = mobile
        self.group = group

    def __repr__(self):
        """查询返回的字段"""
        return str({
            "user_id": self.user_id,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "mobile": self.mobile,
            "group": self.group
        })

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id

    def set_password(self, password):
        """hash密码"""
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        """将password hash以后与数据库的密码比较 一致时返回True"""
        return check_password_hash(self.password, password)


# 定义获取登录用户对象的方法, 必须要有此方法。
@login_manager.user_loader
def load_user(user_id):
    user = CalendarUsers.query.filter(CalendarUsers.user_id == int(user_id)).first()
    return user


class AnonymousUser(AnonymousUserMixin):
    """未登录用户类"""
    # confirmed = False
    @property
    def confirmed(self):
        return False

    @property
    def is_authenticated(self):
        return False

    @property
    def is_active(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return
