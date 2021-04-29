from flask import render_template, request, flash, redirect, Blueprint
from flask_login import current_user

from calendar_config import app
from libs.calendar.about_time import AboutTime
from libs.calendar.calendar_control import NotesManage

pub_calendar = Blueprint("pub_calendar", __name__)


@pub_calendar.route("/pub/", methods=['POST', 'GET'])
def pub_index_publish():
    """
    首页，重定向到当前月份
    :return:
    """
    # print("用户状态*************", current_user, current_user.is_active, current_user.is_authenticated,
    #       current_user.is_anonymous)
    emsg = None
    log_message = str({"rout_url": "pub_calendar.pub_index_publish", "result": "success", "emsg": emsg,
                       "user_ip": request.remote_addr})
    app.logger.info(log_message)
    return redirect("/pub/show_calendar/{}".format(AboutTime().get_today_year_month()))


@pub_calendar.route("/pub/show_calendar/", methods=["POST", "GET"])
def pub_redirect_calendar():
    """
    将表单选中的年月作为参数传到url
    :return:
    """
    emsg = None
    if request.method == 'POST':
        select_year, select_month = request.values.get("select_year"), request.values.get("select_month")
        re_url = "/pub/show_calendar/{}".format(select_year + "-" + select_month)
        log_message = str({"rout_url": "pub_calendar.pub_redirect_calendar", "result": re_url, "emsg": emsg,
                           "user_ip": request.remote_addr})
        app.logger.info(log_message)
        return redirect(re_url)
    log_message = str({"rout_url": "pub_calendar.pub_redirect_calendar", "result": "success", "emsg": emsg,
                       "user_ip": request.remote_addr})
    app.logger.info(log_message)
    return redirect("/pub/")


# 展示本月日历
@pub_calendar.route("/pub/show_calendar/<string:today_year_month>", methods=["POST", "GET"])
def pub_show_calendar(today_year_month):
    """
    根据不同年月展示指定月份
    :param today_year_month: 指定的年月 格式：year-month
    :return:
    """
    emsg = None
    now_year, now_month, now_day = AboutTime().get_today_year_month_day()
    today_date = str(now_year) + "-" + str(now_month) + "-"  # 年份月份格式
    year_selections = [year for year in range(now_year - 1, now_year + 2)]  # 年份下拉框
    month_selections = [month for month in range(1, 13)]  # 月份下拉框
    # 返回当月
    if today_year_month == str(now_year) + "-" + str(now_month):
        days_list, now_year, now_month = NotesManage().pub_get_this_month_notes(year_month=today_year_month)
        log_message = str({"rout_url": "pub_calendar.pub_show_calendar",
                           "result": "/pub/show_calendar/{}， 当月日历显示".format(today_year_month), "emsg": str({
                "days_list": days_list, "now_year": now_year, "now_month": now_month, "today_date": today_date,
                "year_selections": year_selections, "month_selections": month_selections}),
                           "today_year_month": today_year_month, "user_ip": request.remote_addr})
        app.logger.info(log_message)
        return render_template("calendar/calendar_pub_show_calendar.html", days_list=days_list, today_date=today_date,
                               today=now_day,
                               show_today=now_day, year_selections=year_selections, show_year_month=today_date,
                               month_selections=month_selections)
    else:  # 指定年月
        select_year, select_month = int(today_year_month.split("-")[0]), int(today_year_month.split("-")[1])
        show_year_month = today_year_month + "-"
        show_today = 0  # 展示今天特殊标记
        if select_year == now_year and select_month == now_month:
            show_today = now_day
        days_list, year, month = NotesManage().pub_get_this_month_notes(year_month=today_year_month)
        log_message = str({"rout_url": "pub_calendar.pub_show_calendar",
                           "result": "/pub/show_calendar/{}, 指定年月日历显示".format(today_year_month), "emsg": str({
                "days_list": days_list, "now_year": now_year, "now_month": now_month, "today_date": today_date,
                "year_selections": year_selections, "month_selections": month_selections}),
                           "today_year_month": today_year_month, "show_today": show_today,
                           "user_ip": request.remote_addr})
        app.logger.info(log_message)
        return render_template("calendar/calendar_pub_show_calendar.html", days_list=days_list, today_date=today_date,
                               today=now_day,
                               show_today=show_today, year_selections=year_selections, show_year_month=show_year_month,
                               month_selections=month_selections)


# 显示备注  以消息的方法展现
@pub_calendar.route("/pub/note_show/<string:notedate>/", methods=["POST", "GET"])
def pub_calendar_add_note(notedate):
    """
    根据noteday 日期天数 查询当天的记录
    :param noteday: 日期天数
    :return: 有message就flask，没有就刷新日历页面 /show_calendar/
    """
    emsg = None
    notesday = []
    the_year, the_month, the_day = str(notedate).split("-")
    today_notes = NotesManage().pub_get_today_notes(year=str(the_year), month=str(the_month), day=str(the_day))
    for today_note in today_notes:
        notesday.append({"date": the_day, "note": today_note.note, "noteid": str(today_note.id)})
    if notesday:
        log_message = str({"rout_url": "pub_calendar.pub_calendar_add_note", "result": notesday, "emsg": emsg,
                           "user_ip": request.remote_addr})
        app.logger.info(log_message)
        flash(message=notesday)
    show_month = the_year + "-" + the_month
    log_message = str({"rout_url": "pub_calendar.pub_calendar_add_note", "result": "重定向地址：{}".format(
        "/pub/show_calendar/{}".format(show_month)), "emsg": emsg, "user_ip": request.remote_addr})
    app.logger.info(log_message)
    return redirect("/pub/show_calendar/{}".format(show_month))


@pub_calendar.route("/pub/add/<string:notedate>/", methods=["POST", "GET"])
def pub_calendar_add(notedate):
    """
    给指定日期添加note
    :param notedate: 指定日期，年月日
    :return:
    """
    emsg = None
    if request.method == "POST":
        note = request.values.get("note")
        the_year, the_month, the_day = str(notedate).split("-")
        if current_user.is_anonymous:  # 未登录时，用户名为ip地址
            create_user = request.remote_addr
        else:  # 已登录时，用户名为账号名
            create_user = current_user.username
        NotesManage().pub_create_note(note=note, note_year=the_year, note_month=the_month, note_day=the_day,
                                      create_user=create_user, create_ip=request.remote_addr,
                                      update_user=create_user)
        log_message = str({"rout_url": "pub_calendar.pub_calendar_add", "result": "add note success", "emsg": emsg,
                           "note": note, "create_user": create_user, "year": the_year,
                          "month": the_month, "day": the_day, "user_ip": request.remote_addr})
        app.logger.info(log_message)
        return redirect("/pub/show_calendar/{}".format(notedate.split("-")[0] + "-" + notedate.split("-")[1]))
    return render_template("calendar/calendar_pub_note_add.html", notedate=notedate)


@pub_calendar.route("/pub/change_note/<string:notedate>-<string:noteid>/", methods=["POST", "GET"])
def pub_change_note(notedate, noteid):
    """
    根据noteid 获取当前note 的id，date，info。重定向到pub_save_change_note，带上参数
    :param notedate: 时间
    :param noteid: id
    :return:
    """
    emsg = None
    # 根据id查询现在的note
    note_info = NotesManage().pub_get_note_by_id(note_id=noteid)
    log_message = str({"rout_url": "pub_calendar.pub_change_note", "result": "get note success", "emsg": emsg,
                       "note_info": note_info, "user_ip": request.remote_addr})
    app.logger.info(log_message)
    # 重定向   返回id和note
    return render_template("calendar/calendar_change_note.html", noteid=noteid, note_date=notedate,
                           note_info=note_info.note)


# 更改note
@pub_calendar.route("/pub/save_new_note/<string:notedate>-<string:noteid>/", methods=["POST", "GET"])
def pub_save_change_note(notedate, noteid):
    """
    根据id修改note。 notedate只是显示在url中便于区分
    :param notedate: 时间 年月日 str
    :param noteid: id str
    :return: 当前月份日历显示
    """
    emsg = None
    if request.method == "POST":
        new_note_info = request.values.get("new_note")
        if new_note_info:
            NotesManage().pub_update_note(noteid=noteid, new_note=new_note_info, update_ip=request.remote_addr)
            log_message = str({"rout_url": "pub_calendar.pub_save_change_note", "result": "update note success",
                               "emsg": emsg, "noteid": noteid, "new_note_info": new_note_info, "user_ip": request.remote_addr})
            app.logger.info(log_message)
            return redirect("/pub/show_calendar/")
    return "not post"


# 测试
@pub_calendar.route("/pub/1", methods=["POST", "GET"])
def pub_d1():
    # 当月数据存储
    res = NotesManage().pub_get_all_month_notes(year="2021", month="4")
    print(res)
    return str(res)
