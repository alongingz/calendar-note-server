import pymysql

# 不写这个会报：ModuleNotFoundError: No module named 'MySQLdb'
pymysql.install_as_MySQLdb()
