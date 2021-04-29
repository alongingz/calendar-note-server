from calendar_config import app
from views.calendar.pub_calendar import pub_calendar
from views.calendar.user_calendar import user_calendar
from views.public_auth import auth
from views.public_pub import calendar_pub_view
from gevent import pywsgi

app.register_blueprint(auth)  # 用户相关
app.register_blueprint(calendar_pub_view)  # 公用
app.register_blueprint(pub_calendar)  # 公用日历
app.register_blueprint(user_calendar)  # 个人日历

if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5000, debug=True)
    server = pywsgi.WSGIServer(("0.0.0.0", 5004), app)  # 启动ip和端口
    server.serve_forever()  # 监听
