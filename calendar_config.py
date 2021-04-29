from datetime import timedelta

from flask import Flask, g
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from libs.about_log import GetLog


app = Flask(__name__)
app.secret_key = "heiheihaha"  # 表单交互使用，防止跨域攻击
app.permanent_session_lifetime = timedelta(hours=8)  # session有效期

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.remember_cookie_duration = timedelta(hours=8)  # cookie默认有效期是一年
login_manager.login_view = 'auth.login'  # 默认登录视图
login_manager.login_message_category = 'info'  # 登录消息等级
login_manager.login_message = 'Access denied.'
login_manager.session_protection = "strong"  # 提供不同的安全等级防止用户会话遭篡改 默认：'basic'， 可选：strong， None

# 数据库配置  需要提前创建数据库：
mysql_conf = {
    "host": "127.0.0.1",
    "port": 13306,
    "user": "root",
    "password": 123456,
    "database": "calendar_notes",
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}:{}/{}'.format(mysql_conf['user'],
            mysql_conf['password'], mysql_conf['host'], mysql_conf['port'], mysql_conf['database'], )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 查询时是否显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = False
db = SQLAlchemy(app)

# 日志位置和名称，创建log对象. 只需要设置日志存储位置即可，使用flask内置的app.logger.info() 记录日志信息
log = GetLog(log_path="./logs", log_filename="calendar_notes").log()
