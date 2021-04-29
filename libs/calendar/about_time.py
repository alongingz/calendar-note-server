import time
import datetime
import calendar


class AboutTime:
    def get_today_year_month(self):
        now_year, now_month, now_day = AboutTime().get_today_year_month_day()
        today_year_month = str(now_year) + "-" + str(now_month)  # 年份月份格式
        return today_year_month

    def get_today_year_month_day(self):
        now_year, now_month, now_day = time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday  # 当前年月日
        return now_year, now_month, now_day

    def get_now_time(self):
        now_time = datetime.datetime.now()
        return now_time

    # 根据指定年，月获取当月展示数据列表
    def get_calendar_show(self, year, month):
        year, month = int(year), int(month)
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


if __name__ == '__main__':
    a = AboutTime()
    print(a.get_now_time())
    print(a.get_today_year_month())
    print(a.get_today_year_month_day())
    print(a.get_calendar_show(year=2021, month=4))







