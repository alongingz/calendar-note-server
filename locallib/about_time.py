import time
import datetime
import calendar


# 封装关于时间的方法
from locallib.database_sqlite3 import PubNote


class AboutTime:
    def now_year_month_day(self):
        now_year, now_month, now_day = time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday  # 当前年月日
        return now_year, now_month, now_day

    def now_time(self):
        now_time = datetime.datetime.now()
        return now_time

    # 根据指定年，月获取当月展示数据列表
    def get_calendar_show(self, year, month):
        first_day_weekday = datetime.datetime(year=year, month=month, day=1).isoweekday()  # 本月1号是周几
        this_month_lenth = calendar.monthrange(year=year, month=month)[-1]  # 指定月份有多少天
        days_list = []  # 以周为单位的展示列表
        ini_index = 0
        l = [day for day in range(1, this_month_lenth + 1)]  # 本月天数列表  [1,2,3,...,28/29/30/31]
        # 当月1号不是周一，将本周前几天补充为day=0
        if first_day_weekday != 1:
            for i in range(1, first_day_weekday):
                days_list.append({"index": ini_index, "year": year, "month": month, "day": 0})
                ini_index += 1
        # 将本月实际天数添加到一周为单位的展示列表内
        for day in l:
            days_list.append({"index": ini_index, "year": year, "month": month, "day": day})
            ini_index += 1
        return days_list, year, month

    # 查询已有备忘，将指定年月的每一天添加是否有备忘记录
    def get_calendar_show_add_noteday(self, year, month):
        days_list, year, month = self.get_calendar_show(year, month)
        noted_days_list = list(PubNote().filter_date())
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












