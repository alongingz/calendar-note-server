from flask import render_template, request, flash, redirect, Blueprint

from locallib.about_time import AboutTime
from locallib.database_sqlite3 import PubNote

pub_calendar = Blueprint("pub_calendar", __name__)


@pub_calendar.route("/pub/", methods=['POST', 'GET'])
def index_publish():
    now_year, now_month, now_day = AboutTime().now_year_month_day()
    today_year_month = str(now_year) + "-" + str(now_month)  # 年份月份格式
    return redirect("/pub/show_calendar/{}".format(today_year_month))


@pub_calendar.route("/pub/show_calendar/", methods=["POST", "GET"])
def redirect_calendar():
    """
    将表单选中的年月作为参数传到url
    :return:
    """
    if request.method == 'POST':
        select_year, select_month = request.values.get("select_year"), request.values.get("select_month")
        return redirect("/pub/show_calendar/{}".format(select_year + "-" + select_month))
    return redirect("/pub/")


# 展示日历, 展示本月和下月的日历
@pub_calendar.route("/pub/show_calendar/<string:today_year_month>", methods=["POST", "GET"])
def show_calendar(today_year_month):
    """
    根据不同年月展示指定月份
    :param today_year_month: 指定的年月 格式：year-month
    :return:
    """
    now_year, now_month, now_day = AboutTime().now_year_month_day()
    today_date = str(now_year) + "-" + str(now_month) + "-"  # 年份月份格式
    year_selections = [year for year in range(now_year - 1, now_year + 2)]  # 年份下拉框
    month_selections = [month for month in range(1, 13)]  # 月份下拉框
    # 返回当月
    if today_year_month == str(now_year) + "-" + str(now_month):
        days_list, now_year, now_month = AboutTime().get_calendar_show_add_noteday(year=now_year, month=now_month)
        return render_template("pub_show_calendar.html", days_list=days_list, today_date=today_date, today=now_day,
                               show_today=now_day, year_selections=year_selections, show_year_month=today_date,
                               month_selections=month_selections)
    else:
        select_year, select_month = int(today_year_month.split("-")[0]), int(today_year_month.split("-")[1])
        show_year_month = today_year_month + "-"
        show_today = 0  # 展示今天特殊标记
        if select_year == now_year and select_month == now_month:
            show_today = now_day
        days_list, year, month = AboutTime().get_calendar_show_add_noteday(year=select_year, month=select_month)
        return render_template("pub_show_calendar.html", days_list=days_list, today_date=today_date, today=now_day,
                               show_today=show_today, year_selections=year_selections, show_year_month=show_year_month,
                               month_selections=month_selections)


# 显示备注  以消息的方法展现 Todo 不同月份备忘显示
@pub_calendar.route("/pub/note_show/<string:notedate>/", methods=["POST", "GET"])
def calendar_add_note(notedate):
    """
    根据noteday 日期天数 查询当天的记录
    :param noteday: 日期天数
    :return: 有message就flask，没有就刷新日历页面 /show_calendar/
    """
    notesday = []
    the_year, the_month, the_day = str(notedate).split("-")
    result = PubNote().get_note(date=notedate)
    print(result)
    for notes_theday, notes in result:
        notesday.append({"date": notes_theday, "note": notes})
    flash(message=notesday)
    show_month = the_year + "-" + the_month
    return redirect("/pub/show_calendar/{}".format(show_month))


@pub_calendar.route("/pub/add/<string:notedate>/", methods=["POST", "GET"])
def calendar_add(notedate):
    if request.method == "POST":
        note = request.values.get("note")
        PubNote().insert_note(date=notedate, note=note)
        return redirect("/pub/show_calendar/{}".format(notedate.split("-")[0] + "-" + notedate.split("-")[1]))
    return render_template("pub_note_add.html", notedate=notedate)
