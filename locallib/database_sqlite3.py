# sqlite3数据增删改查
import sqlite3

from config import pub_notes_table_name, users_table_name, user_notes_table_name


class PubNote:
    """
    CREATE TABLE IF NOT EXISTS 'pub_notes' (id integer primary key autoincrement not null, date text, note text);
    """

    def __init__(self):
        self.cnn = sqlite3.connect(database="calendar_notes.sqlite3")
        self.cur = self.cnn.cursor()
        self.table = pub_notes_table_name

    def get_all(self):
        res = self.cur.execute("select date, note from {};".format(self.table))
        return res.fetchall()

    def get_note(self, date):
        try:
            res = self.cur.execute("select id, date, note from {} where date='{}';".format(self.table, date))
            return res.fetchall()
        except Exception as e:
            self.cnn.rollback()

    def get_note_by_id(self, noteid):
        try:
            res = self.cur.execute("select id, date, note from {} where id={};".format(self.table, int(noteid)))
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

    def update_note(self, noteid, new_note):
        try:
            self.cur.execute(
                "update {} set note='{}' where id={};".format(self.table, new_note, int(noteid)))
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


class UserNote:
    """
    CREATE TABLE IF NOT EXISTS 'user_notes' (id integer primary key autoincrement not null, username text, date text, note text);
    """

    def __init__(self):
        self.cnn = sqlite3.connect(database="calendar_notes.sqlite3")
        self.cur = self.cnn.cursor()
        self.table = user_notes_table_name

    def get_all(self):
        res = self.cur.execute("select username, date, note from {};".format(self.table))
        return res.fetchall()

    def get_note(self, username, date):
        try:
            res = self.cur.execute("select username, date, note from {} where username='{}' and  date='{}';".format(
                self.table, username, date))
            return res.fetchall()
        except Exception as e:
            self.cnn.rollback()

    def insert_note(self, username, date, note):
        try:
            self.cur.execute("insert into {} (username, date, note) values ('{}', '{}', '{}');".format(self.table, username, date, note))
            self.cnn.commit()
            print("插入成功")
        except Exception as e:
            self.cnn.rollback()

    def update_note(self, username, date, old_note, new_note):
        try:
            self.cur.execute(
                "update {} set note='{}' where username='{}' and date='{}' and old_note='{}';".format(self.table, new_note, username, date, old_note))
            self.cnn.commit()
        except Exception as e:
            self.cnn.rollback()

    def delete_note(self, username, date):
        try:
            self.cur.execute("delete from {} where username='{}' and date='{}';".format(self.table, username, date))
            self.cnn.commit()
        except Exception as e:
            self.cnn.rollback()

    def filter_date(self):
        date_notes = self.get_all()
        noted_dates_list = []
        for username, date, note in date_notes:
            if note:
                noted_dates_list.append(date)
        return set(noted_dates_list)


class UserInfo:
    def __init__(self):
        """
        create table users (id integer primary key autoincrement not null, username text not null, password text not null);
        """
        self.cnn = sqlite3.connect(database="calendar_notes.sqlite3")
        self.cur = self.cnn.cursor()
        self.table = users_table_name

    # 用户注册
    def create_user(self, username, password):
        try:
            self.cur.execute(
                "insert into {} (username, password) values('{}', '{}');".format(self.table, username, password))
            self.cnn.commit()
            return True
        except:
            self.cnn.rollback()
            return False

    # 查询用户是否存在
    def get_userinfo(self, username):
        result = self.cur.execute("select username, password from {} where username='{}';".format(self.table, username))
        result = result.fetchall()
        if result:
            return result  # username， password
        else:
            return False
