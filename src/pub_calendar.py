from flask import render_template, request, flash, redirect, Blueprint

from locallib.about_time import AboutTime
from locallib.database_sqlite3 import PubNote

pub_calendar = Blueprint("pub_calendar", __name__)


@pub_calendar.route("/pub/", methods=['POST', 'GET'])
def pub_index_publish():
    """
    首页，重定向到当前月份
    :return:
    """
    now_year, now_month, now_day = AboutTime().now_year_month_day()
    today_year_month = str(now_year) + "-" + str(now_month)  # 年份月份格式
    return redirect("/pub/show_calendar/{}".format(today_year_month))


@pub_calendar.route("/pub/show_calendar/", methods=["POST", "GET"])
def pub_redirect_calendar():
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
def pub_show_calendar(today_year_month):
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
def pub_calendar_add_note(notedate):
    """
    根据noteday 日期天数 查询当天的记录
    :param noteday: 日期天数
    :return: 有message就flask，没有就刷新日历页面 /show_calendar/
    """
    notesday = []
    the_year, the_month, the_day = str(notedate).split("-")
    result = PubNote().get_note(date=notedate)
    for id, notes_theday, notes in result:
        notesday.append({"date": notes_theday, "note": notes, "noteid": str(id)})
    flash(message=notesday)
    show_month = the_year + "-" + the_month
    return redirect("/pub/show_calendar/{}".format(show_month))


@pub_calendar.route("/pub/add/<string:notedate>/", methods=["POST", "GET"])
def pun_calendar_add(notedate):
    """
    给指定日期添加note
    :param notedate: 指定日期，年月日
    :return:
    """
    if request.method == "POST":
        note = request.values.get("note")
        PubNote().insert_note(date=notedate, note=note)
        return redirect("/pub/show_calendar/{}".format(notedate.split("-")[0] + "-" + notedate.split("-")[1]))
    return render_template("pub_note_add.html", notedate=notedate)


@pub_calendar.route("/pub/change_note/<string:notedate>-<string:noteid>/", methods=["POST", "GET"])
def pub_change_note(notedate, noteid):
    """
    根据noteid 获取当前note 的id，date，info。重定向到pub_save_change_note，带上参数
    :param notedate: 时间
    :param noteid: id
    :return:
    """
    # 根据id查询现在的note
    note_id, note_date, note_info = PubNote().get_note_by_id(noteid=noteid)[0]
    # 重定向   返回id和note
    return render_template("change_note.html", noteid=noteid, note_date=note_date, note_info=note_info)


# 更改note
@pub_calendar.route("/pub/save_new_note/<string:notedate>-<string:noteid>/", methods=["POST", "GET"])
def pub_save_change_note(notedate, noteid):
    """
    根据id修改note。 notedate只是显示在url中便于区分
    :param notedate: 时间 年月日 str
    :param noteid: id str
    :return: 当前月份日历显示
    """
    if request.method == "POST":
        new_note_info = request.values.get("new_note")
        if new_note_info:
            PubNote().update_note(noteid=noteid, new_note=new_note_info)
            return redirect("/pub/show_calendar/")
    return "not post"

