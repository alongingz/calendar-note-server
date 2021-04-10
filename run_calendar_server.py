from flask import Flask, render_template, request, flash, redirect
import calendar
import datetime
import time
import sqlite3

app = Flask(__name__)
app.secret_key = 'nihsiwodexiaoyaxiaopingguo'


class Sqlite3Excute:
    def __init__(self):
        self.cnn = sqlite3.connect(database="calendar_notes.sqlite3")
        self.cur = self.cnn.cursor()
        self.table = "notes"

    def get_all(self):
        res = self.cur.execute("select date, note from {};".format(self.table))
        return res.fetchall()

    def get_note(self, date):
        try:
            print("select note from {} where date={};".format(self.table, date))
            res = self.cur.execute("select note from {} where date='{}';".format(self.table, date))
            return res.fetchall()
        except Exception as e:
            self.cnn.rollback()

    def insert_note(self, date, note):
        try:
            self.cur.execute("insert into {} (date, note) values ('{}', '{}');".format(self.table, date, note))
            self.cnn.commit()
            print("插入成功")
        except Exception as e:
            self.cnn.rollback()

    def update_note(self, date, new_date, new_note):
        try:
            self.cur.execute(
                "update {} set date='{}', note='{}' where date='{}';".format(self.table, new_date, new_note, date))
            self.cnn.commit()
        except Exception as e:
            self.cnn.rollback()

    def delete_note(self, date):
        try:
            self.cur.execute("delete from {} where date='{}';".format(self.table, date))
            self.cnn.commit()
        except Exception as e:
            self.cnn.rollback()

    def filter_date(self):
        date_notes = self.get_all()
        noted_dates_list = []
        for date, note in date_notes:
            if note:
                noted_dates_list.append(date)
        return set(noted_dates_list)


# 封装关于时间的方法
class AboutTime:
    @staticmethod
    def now_year_month_day():
        now_year, now_month, now_day = time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday  # 当前年月日
        return now_year, now_month, now_day

    @staticmethod
    def now_time():
        now_time = datetime.datetime.now()
        return now_time


# 日历提醒功能
def get_calendar_show(year, month):
    first_day_weekday = datetime.datetime(year=year, month=month, day=1).isoweekday()  # 本月1号是周几
    this_month_lenth = calendar.monthrange(year=year, month=month)[-1]  # 指定月份有多少天
    days_list = []
    ini_index = 0
    l = [day for day in range(1, this_month_lenth + 1)]  # 本月天数列表
    if first_day_weekday != 1:
        for i in range(1, first_day_weekday):
            days_list.append({"index": ini_index, "year": year, "month": month, "day": 0})
            ini_index += 1
    for day in l:
        days_list.append({"index": ini_index, "year": year, "month": month, "day": day})
        ini_index += 1
    # print(days_list)
    return days_list, year, month


# 将当月日期添加是否有note记录
def get_calendar_show_add_noteday(year, month):
    days_list, year, month = get_calendar_show(year, month)
    noted_days_list = list(Sqlite3Excute().filter_date())
    # 先将本月所有天数 设置为无备忘状态
    for d in days_list:
        d['is_note_day'] = False
    # 指定年月日有数据时，才更改状态
    for ds in noted_days_list:
        for items in days_list:
            if items['year'] == int(ds.split("-")[0]) and items['month'] == int(ds.split("-")[1]) and \
                    items['day'] == int(ds.split("-")[-1]):
                items['is_note_day'] = True
    return days_list, year, month


@app.route("/")
def index():
    now_year, now_month, now_day = AboutTime().now_year_month_day()
    today_year_month = str(now_year) + "-" + str(now_month)  # 年份月份格式
    return redirect("/show_calendar/{}".format(today_year_month))


@app.route("/show_calendar/", methods=["POST", "GET"])
def redirect_calendar():
    """
    将表单选中的年月作为参数传到url
    :return:
    """
    if request.method == 'POST':
        select_year, select_month = request.values.get("select_year"), request.values.get("select_month")
        return redirect("/show_calendar/{}".format(select_year + "-" + select_month))
    return redirect("/")


# 展示日历, 展示本月和下月的日历
@app.route("/show_calendar/<string:today_year_month>", methods=["POST", "GET"])
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
        days_list, now_year, now_month = get_calendar_show_add_noteday(year=now_year, month=now_month)
        return render_template("show_calendar.html", days_list=days_list, today_date=today_date, today=now_day,
                               show_today=now_day, year_selections=year_selections, show_year_month=today_date,
                               month_selections=month_selections)
    else:
        select_year, select_month = int(today_year_month.split("-")[0]), int(today_year_month.split("-")[1])
        show_year_month = today_year_month + "-"
        show_today = 0  # 展示今天特殊标记
        if select_year == now_year and select_month == now_month:
            show_today = now_day
        days_list, year, month = get_calendar_show_add_noteday(year=select_year, month=select_month)
        return render_template("show_calendar.html", days_list=days_list, today_date=today_date, today=now_day,
                               show_today=show_today, year_selections=year_selections, show_year_month=show_year_month,
                               month_selections=month_selections)


# 显示备注  以消息的方法展现 Todo 不同月份备忘显示
@app.route("/note_show/<string:notedate>/", methods=["POST", "GET"])
def calendar_add_note(notedate):
    """
    根据noteday 日期天数 查询当天的记录
    :param noteday: 日期天数
    :return: 有message就flask，没有就刷新日历页面 /show_calendar/
    """
    notesday = []
    now_year, now_month, today = str(notedate).split("-")
    notes_all = Sqlite3Excute().get_all()
    for date, note in notes_all:
        year, month, day = str(date).split("-")
        if now_year == year and now_month == month and today == day:
            notesday.append(note)
    flash(message=notesday)
    show_month = now_year + "-" + now_month
    return redirect("/show_calendar/{}".format(show_month))


@app.route("/add/<string:notedate>/", methods=["POST", "GET"])
def calendar_add(notedate):
    if request.method == "POST":
        note = request.values.get("note")
        Sqlite3Excute().insert_note(date=notedate, note=note)
        return redirect("/show_calendar/{}".format(notedate.split("-")[0] + "-" + notedate.split("-")[1]))
    return render_template("note_add.html", notedate=notedate)


# @app.route("/1/", methods=['POST', 'GET'])
# def demo1():
#     res = Sqlite3Excute().filter_date()
#     return str(res)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
