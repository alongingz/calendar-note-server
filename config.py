# default ip, port
default_ip = "0.0.0.0"
default_port = 5000

# database config
database_name = "calendar_notes.sqlite3"
pub_notes_table_name = "pub_notes"
user_notes_table_name = "user_notes"
users_table_name = "users"

# the sql for create table
create_pub_notes_sql = "CREATE TABLE IF NOT EXISTS 'pub_notes' (id integer primary key autoincrement not null, " \
                       "date text, note text);"
create_users_sql = "create table IF NOT EXISTS users (id integer primary key autoincrement not null, username text not null, " \
                   "password text not null);"
create_user_notes_sql = "CREATE TABLE IF NOT EXISTS 'user_notes' (id integer primary key autoincrement not null, " \
                        "username text not null, date text not null, note text not null);"
