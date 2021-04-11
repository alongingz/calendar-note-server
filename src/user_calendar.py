from flask import Flask, Blueprint, request, redirect, render_template

user_calendar = Blueprint(name="user_calendar", import_name=__name__)


@user_calendar.route("/", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        username = request.values.get("username")
        password1 = request.values.get("password1")
        password2 = request.values.get("password2")
        if password1 != password2:
            return render_template("index.html", error_message="两次密码不一致")
        elif not username:  # 用户未注册, 查询用户是否存在
            # 新用户，注册，并进入首页，显示当天日历
            pass
        elif username != password1:
            # 老用户检验密码错误，提示错误信息
            pass
        else:
            # 老用户校验密码正确，显示当天日历
            pass
        now_year, now_month, now_day = AboutTime().now_year_month_day()
        today_year_month = str(now_year) + "-" + str(now_month)  # 年份月份格式
        return redirect("/show_calendar/{}/{}".format(username, today_year_month))
    return render_template("index.html")



