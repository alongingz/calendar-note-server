import pymysql


class LocalhostMysql:
    def __init__(self, **kwargs):
        # QA
        # self.host = '192.168.1.145'
        # self.user = 'work'
        # self.password = '5Zp5wph2Ol1P'

        # 本地
        self.host = '127.0.0.1'
        self.user = 'root'
        self.password = '123456'
        pymysql.install_as_MySQLdb()

    def select_data(self, database, sql):
        self.connect = pymysql.connect(host=self.host, port=3306, user=self.user, password=self.password, db=database,
                                       charset='utf8mb4',
                                       cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connect.cursor()
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            result = self.cursor.fetchall()
            print('sql成功：', result)
            return result
        except Exception as e:
            self.connect.rollback()
            print('sql失败， 已回滚', e)
            return 0
        finally:
            self.cursor.close()
            self.connect.close()


if __name__ == '__main__':
    pass
