import datetime
from calendar_config import db


class PubNotes(db.Model):
    """通用记录"""
    id = db.Column(db.Integer, autoincrement=True, unique=True, primary_key=True, comment="id")
    note = db.Column(db.String(length=255), comment="公共记录")
    note_year = db.Column(db.String(length=10), comment="记录对应的年")
    note_month = db.Column(db.String(length=10), comment="记录对应的月")
    note_day = db.Column(db.String(length=10), comment="记录对应的日")
    create_time = db.Column(db.DateTime(), default=datetime.datetime.now, comment="创建时间")
    create_user = db.Column(db.String(length=255), comment="创建人")
    update_time = db.Column(db.DateTime(), default=datetime.datetime.now, comment="更新时间")
    update_user = db.Column(db.String(length=255), comment="最后更改人")
    update_ip = db.Column(db.String(length=255), comment="最后更该人ip")

    def __repr__(self):
        """查询返回字段"""
        return str({
            "id": self.id,
            "note": self.note,
            "note_year": self.note_year,
            "note_month": self.note_month,
            "note_day": self.note_day,
            "create_time": self.create_time,
            "create_user": self.create_user,
            "update_time": self.update_time,
            "update_user": self.update_user,
            "update_ip": self.update_ip,
        })

    def __init__(self, note, note_year, note_month, note_day, create_user, update_user, update_ip):
        self.note = note
        self.note_year = note_year
        self.note_month = note_month
        self.note_day = note_day
        self.create_user = create_user
        self.update_user = update_user
        self.update_ip = update_ip


class UserNotes(db.Model):
    """个人记录"""
    id = db.Column(db.Integer, autoincrement=True, unique=True, primary_key=True, comment="id")
    username = db.Column(db.String(length=255), comment="用户名")
    note = db.Column(db.String(length=255), comment="个人记录")
    note_year = db.Column(db.String(length=10), comment="记录对应的年")
    note_month = db.Column(db.String(length=10), comment="记录对应的月")
    note_day = db.Column(db.String(length=10), comment="记录对应的日")
    create_time = db.Column(db.DateTime(), default=datetime.datetime.now, comment="创建时间")
    update_time = db.Column(db.DateTime(), default=datetime.datetime.now, comment="更新时间")
    update_ip = db.Column(db.String(length=255), comment="最后更该人ip")

    def __repr__(self):
        """查询返回字段"""
        return str({
            "id": self.id,
            "username": self.username,
            "note": self.note,
            "note_year": self.note_year,
            "note_month": self.note_month,
            "note_day": self.note_day,
            "create_time": self.create_time,
            "update_time": self.update_time,
            "update_ip": self.update_ip,
        })

    def __init__(self, username, note, note_year, note_month, note_day, update_ip):
        self.username = username
        self.note = note
        self.note_year = note_year
        self.note_month = note_month
        self.note_day = note_day
        self.update_ip = update_ip











