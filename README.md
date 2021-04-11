# calendar-note-server
calendar-note 备忘录功能

## database
sqlite3: calendat_notes.sqlite3

table: CREATE TABLE IF NOT EXISTS 'notes' (id integer primary key autoincrement not null, date text, note text);

## 简介
使用python3，flask框架和sqlite3数据库制作的一款简单的记事本备忘录功能
### 使用
1、git clone https://github.com/alongingz/calendar-note-server.git

2、calendar-note-server 目录下执行： python3 start-calendar-server.py 将会使用nohup 在后台运行。注意：此方法只能在linux系统中使用。
如需在Windows系统启动，请使用: python3 calendar_server.py 调试。

3、访问url: http://127.0.0.1:5000/

### 具体功能：

1、显示当月日历，并标记当天日期；

2、标记已有备注的日期；

3、点击日期显示点击日期的备注；

3、点击指定日期的add按钮，添加指定日期的备注