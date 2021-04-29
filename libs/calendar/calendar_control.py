from calendar_config import db
from libs.calendar.about_time import AboutTime
from modules.calendar_days import PubNotes, UserNotes


class NotesManage:
    def __init__(self):
        self.db = db
        self.pubnote = PubNotes
        self.usernotes = UserNotes

    def pub_get_note_by_id(self, note_id):
        """根据id获取note对象，返回的是一个 对象"""
        note = self.pubnote.query.filter(self.pubnote.id == note_id).first()
        print(type(note))
        return note

    def pub_get_today_notes(self, year, month, day):
        """根据年。月。日获取指定某一天的所有记录"""
        today_note = self.pubnote.query.filter(self.pubnote.note_year == year).filter(
            self.pubnote.note_month == month).filter(self.pubnote.note_day == day).all()
        return today_note

    def pub_get_all_month_notes(self, year, month):
        """根据指定年、月 获取指定月份的所有记录"""
        notes_info = self.pubnote.query.filter(self.pubnote.year == year).filter(self.pubnote.month == month).all()
        return notes_info

    def pub_create_note(self, note, note_year, note_month, note_day, create_user, create_ip, update_user):
        """创建记录"""
        new_note_info = self.pubnote(note=note, note_year=note_year, note_month=note_month, note_day=note_day,
                                     create_user=create_user, update_user=update_user, update_ip=create_ip)
        self.db.session.add(new_note_info)
        self.db.session.commit()

    def pub_update_note(self, noteid, new_note, update_ip):
        """更新记录"""
        new_note = new_note.replace(" ", "")  # 如果new_note为一个空格时，替换空格删除数据
        if new_note:  # 替换空格后还有非空字段就更新数据
            # 先查询指定id的记录，查询结果为一条数据对象
            old_note_info = self.pubnote.query.filter(self.pubnote.id == noteid).first()
            # 将数据对象的note值换为新的值
            old_note_info.note = new_note
            # 更新时间和ip
            old_note_info.update_time = AboutTime().get_now_time()
            old_note_info.update_ip = update_ip
        else:  # 删除数据
            note_info = self.pubnote.query.filter(self.pubnote.id == noteid).first()
            db.session.delete(note_info)
        # 提交修改
        self.db.session.commit()

    def pub_get_this_month_notes(self, year_month):
        """根据日历展示  获取指定月份是否包含记录"""
        year, month = str(year_month).split("-")
        days_list, year, month = AboutTime().get_calendar_show(year=year, month=month)
        # print(days_list)
        # 将本月所有天数设置为无记录状态
        for day in days_list:
            day['is_note_day'] = False
        # 指定天数有记录时，设置为true
        for calendar_day in days_list:
            d = self.pub_get_today_notes(year=calendar_day['year'], month=calendar_day['month'],
                                         day=calendar_day['day'])
            if d:
                calendar_day['is_note_day'] = True
        return days_list, year, month

    def user_get_note_by_id(self, username, note_id):
        """根据username 和 id获取note对象，返回的是一个 对象"""
        note = self.usernotes.query.filter(self.usernotes.username == username).filter(self.usernotes.id == note_id).first()
        print(type(note))
        return note

    def user_get_today_notes(self, username, year, month, day):
        """根据用户名,年,月,日获取指定某一天的所有记录"""
        today_note = self.usernotes.query.filter(self.usernotes.username == username).filter(self.usernotes.note_year == year).filter(
            self.usernotes.note_month == month).filter(self.usernotes.note_day == day).all()
        return today_note

    def user_create_note(self, username, note, year, month, day, create_ip):
        """创建记录"""
        new_note_info = self.usernotes(username=username, note=note, note_year=year, note_month=month, note_day=day,
                                       update_ip=create_ip)
        self.db.session.add(new_note_info)
        self.db.session.commit()

    def user_update_note(self, username, noteid, new_note, update_ip):
        """更新记录"""
        new_note = new_note.replace(" ", "")  # 如果new_note为一个空格时，替换空格删除数据
        if new_note:  # 替换空格后还有非空字段就更新数据
            # 先查询指定username 和 id的记录，查询结果为一条数据对象
            old_note_info = self.usernotes.query.filter(self.usernotes.username == username).filter(
                self.usernotes.id == noteid).first()
            # 将数据对象的note值换为新的值
            old_note_info.note = new_note
            # 更新时间和ip
            old_note_info.update_time = AboutTime().get_now_time()
            old_note_info.update_ip = update_ip
        else:  # 删除数据
            note_info = self.usernotes.query.filter(self.usernotes.id == noteid).first()
            db.session.delete(note_info)
        # 提交修改
        self.db.session.commit()

    def user_get_this_month_notes(self, username, year_month):
        """根据日历展示  获取指定用户月份是否包含记录"""
        year, month = str(year_month).split("-")
        days_list, year, month = AboutTime().get_calendar_show(year=year, month=month)
        # print(days_list)
        # 将本月所有天数设置为无记录状态
        for day in days_list:
            day['is_note_day'] = False
            day['username'] = username
        # 指定天数有记录时，设置为true
        for calendar_day in days_list:
            d = self.user_get_today_notes(username=username, year=calendar_day['year'], month=calendar_day['month'],
                                         day=calendar_day['day'])
            if d:
                calendar_day['is_note_day'] = True
        return days_list, year, month


