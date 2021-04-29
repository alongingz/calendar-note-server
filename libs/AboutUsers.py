from sqlalchemy import text
from werkzeug.security import generate_password_hash


class AboutUser:
    def __init__(self, db, table_model):
        self.db = db
        self.table_model = table_model

    def create_user(self, username, password, email=None, mobile=None, group=None):
        password = generate_password_hash(password)  # 密码加密
        user = self.table_model(username=username, password=password, email=email, mobile=mobile, group=group)
        self.db.session.add(user)
        self.db.session.commit()

    def get_user_info(self, username):
        # 查询方法一 查询全部用户
        # users = self.table_model.query.all()
        # for user_info in users:
        #     print("----------", type(user_info), user_info)
        #     if user_info.username == username:
        #         return user_info
        # 查询方法二 指定用户名查询
        user_info = self.table_model.query.filter(text("username='{}'".format(username))).all()
        print("________", type(user_info), user_info)
        print("***)______**", type(user_info[0]))
        if username == user_info[0].username:
            return user_info[0]
        return None

