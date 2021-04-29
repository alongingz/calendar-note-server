from flask import Blueprint, request, redirect, render_template, flash
from flask_login import current_user, login_required

from calendar_config import app
from libs.calendar.about_time import AboutTime
from libs.calendar.calendar_control import NotesManage

user_calendar = Blueprint(name="user_calendar", import_name=__name__)


@user_calendar.route("/<string:username>/", methods=['POST', 'GET'])
@login_required
def user_index(username):
    """首页，重定向到当前月份"""
    # print("user_index --- 用户状态*************", current_user, current_user.is_active, current_user.is_authenticated,
    #       current_user.is_anonymous)
    emsg = None
    log_message = str({"rout_url": "user_calendar.user_index", "result": "success", "emsg": emsg,
                       "username": current_user.username, "user_ip": request.remote_addr})
    app.logger.info(log_message)
    return redirect("/{}/show_calendar/{}".format(username, AboutTime().get_today_year_month()))


@login_required
@user_calendar.route("/<string:username>/show_calendar/", methods=["POST", "GET"])
def user_redirect_calendar(username):
    emsg = None
    if request.method == 'POST':
        select_year, select_month = request.values.get("select_year"), request.values.get("select_month")
        re_url = "/{}/show_calendar/{}".format(username, select_year + "-" + select_month)
        log_message = str({"rout_url": "user_calendar.user_redirect_calendar", "result": "success", "emsg": emsg,
                           "url_username": username, "username": current_user.username,
                           "re_url": re_url, "user_ip": request.remote_addr})
        app.logger.info(log_message)
        return redirect(re_url)
    log_message = str({"rout_url": "user_calendar.user_redirect_calendar", "result": "success", "emsg": emsg,
                       "url_username": username, "username": current_user.username, "user_ip": request.remote_addr})
    app.logger.info(log_message)
    return redirect("/{}/".format(username))


# 展示本月日历
@login_required
@user_calendar.route("/<string:username>/show_calendar/<string:today_year_month>", methods=["POST", "GET"])
def user_show_calendar(username, today_year_month):
    now_year, now_month, now_day = AboutTime().get_today_year_month_day()
    today_date = str(now_year) + "-" + str(now_month) + "-"  # 年份月份格式
    year_selections = [year for year in range(now_year - 1, now_year + 2)]  # 年份下拉框
    month_selections = [month for month in range(1, 13)]  # 月份下拉框
    # 返回当月
    if today_year_month == str(now_year) + "-" + str(now_month):
        days_list, now_year, now_month = NotesManage().user_get_this_month_notes(username=username,
                                                                                 year_month=today_year_month)
        log_message = str({"rout_url": "user_calendar.user_show_calendar",
                           "result": "/{}/show_calendar/{}， 当月日历显示".format(username, today_year_month), "emsg": str({
                "days_list": days_list, "now_year": now_year, "now_month": now_month, "today_date": today_date,
                "year_selections": year_selections, "month_selections": month_selections}),
                           "today_year_month": today_year_month, "username": current_user.username,
                          "user_ip": request.remote_addr})
        app.logger.info(log_message)
        return render_template("calendar/calendar_user_show_calendar.html", days_list=days_list, today_date=today_date,
                               today=now_day,
                               show_today=now_day, year_selections=year_selections, show_year_month=today_date,
                               month_selections=month_selections)
    else:
        select_year, select_month = int(today_year_month.split("-")[0]), int(today_year_month.split("-")[1])
        show_year_month = today_year_month + "-"
        show_today = 0  # 展示今天特殊标记
        if select_year == now_year and select_month == now_month:
            show_today = now_day
        days_list, year, month = NotesManage().pub_get_this_month_notes(year_month=today_year_month)
        log_message = str({"rout_url": "user_calendar.user_show_calendar",
                           "result": "/{}/show_calendar/{}, 指定年月日历显示".format(username, today_year_month), "emsg": str({
                "days_list": days_list, "now_year": now_year, "now_month": now_month, "today_date": today_date,
                "year_selections": year_selections, "month_selections": month_selections}),
                           "today_year_month": today_year_month, "show_today": show_today,
                           "username": current_user.username, "user_ip": request.remote_addr})
        app.logger.info(log_message)
        return render_template("calendar/calendar_user_show_calendar.html", days_list=days_list, today_date=today_date,
                               today=now_day,
                               show_today=show_today, year_selections=year_selections, show_year_month=show_year_month,
                               month_selections=month_selections)


# 显示备注  以消息的方法展现
@login_required
@user_calendar.route("/<string:username>/note_show/<string:notedate>/", methods=["POST", "GET"])
def user_calendar_add_note(username, notedate):
    notesday = []
    the_year, the_month, the_day = str(notedate).split("-")
    today_notes = NotesManage().user_get_today_notes(username=username, year=str(the_year), month=str(the_month),
                                                     day=str(the_day))
    for today_note in today_notes:
        notesday.append({"date": the_day, "note": today_note.note, "noteid": str(today_note.id)})
    if notesday:
        log_message = str({"rout_url": "user_calendar.user_calendar_add_note", "result": notesday, "emsg": None,
                           "username": current_user.username, "user_ip": request.remote_addr})
        app.logger.info(log_message)
        flash(message=notesday)
    show_month = the_year + "-" + the_month
    log_message = str({"rout_url": "user_calendar.user_calendar_add_note", "result": "重定向地址：{}".format(
        "/{}/show_calendar/{}".format(username, show_month)), "username": current_user.username, "user_ip": request.remote_addr})
    app.logger.info(log_message)
    return redirect("/{}/show_calendar/{}".format(username, show_month))


@login_required
@user_calendar.route("/<string:username>/add/<string:notedate>/", methods=["POST", "GET"])
def user_calendar_add(username, notedate):
    if request.method == "POST":
        note = request.values.get("note")
        the_year, the_month, the_day = str(notedate).split("-")
        NotesManage().user_create_note(username=username, note=note, year=the_year, month=the_month, day=the_day,
                                       create_ip=request.remote_addr)
        log_message = str({"rout_url": "user_calendar.user_calendar_add", "result": "add note success",
                           "note": note, "username": current_user.username, "year": the_year,
                           "month": the_month, "day": the_day, "user_ip": request.remote_addr})
        app.logger.info(log_message)
        return redirect("/{}/show_calendar/{}".format(username, notedate.split("-")[0] + "-" + notedate.split("-")[1]))
    return render_template("calendar/calendar_user_note_add.html", notedate=notedate)


@login_required
@user_calendar.route("/<string:username>/change_note/<string:notedate>-<string:noteid>/", methods=["POST", "GET"])
def user_change_note(username, notedate, noteid):
    # 根据id查询现在的note
    note_info = NotesManage().user_get_note_by_id(username=username, note_id=noteid)
    log_message = str({"rout_url": "user_calendar.user_change_note", "result": "get note success",
                       "note_info": note_info, "username": current_user.username, "user_ip": request.remote_addr})
    app.logger.info(log_message)
    # 重定向   返回id和note
    return render_template("calendar/calendar_user_change_note.html", noteid=noteid, note_date=notedate,
                           note_info=note_info.note)


# 更改note
@login_required
@user_calendar.route("/<string:username>/save_new_note/<string:notedate>-<string:noteid>/", methods=["POST", "GET"])
def user_save_change_note(username, notedate, noteid):
    if request.method == "POST":
        new_note_info = request.values.get("new_note")
        if new_note_info:
            NotesManage().user_update_note(username=username, noteid=noteid, new_note=new_note_info,
                                           update_ip=request.remote_addr)
            log_message = str({"rout_url": "user_calendar.user_save_change_note", "result": "update note success",
                               "username": current_user.username, "noteid": noteid, "new_note_info": new_note_info,
                               "user_ip": request.remote_addr})
            app.logger.info(log_message)
            return redirect("/{}/show_calendar/".format(username))
    return "not post"
