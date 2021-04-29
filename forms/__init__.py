# from datetime import timedelta
#
# from flask import Flask
# from flask_login import LoginManager
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
# app.secret_key = "heiheihaha"  # 表单交互使用，防止跨域攻击
# app.permanent_session_lifetime = timedelta(days=1)  # session有效期
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'auth.login'  # 默认登录视图
# login_manager.login_message_category = 'info'
# login_manager.login_message = 'Access denied.'
# login_manager.session_protection = "strong"
#
# # 数据库配置
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/flask_calendar'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# # 查询时会显示原始SQL语句
# app.config['SQLALCHEMY_ECHO'] = False
# db = SQLAlchemy(app)
