#_*_ coding: utf-8 _*_

from B2C.DataBase import MysqlDatabase
import datetime

class BlackListDao:
    def __init__(self):
        # 블랙리스트 등록
        self.query_insert_black_list = "INSERT INTO b2c_blacklist (phone_num, reason, regist_user, regist_date, modify_date)" \
                                       "VALUES (%s, %s, %s, %s, %s)"

        # 블랙리스트 업데이트
        self.query_update_black_list = "UPDATE b2c_blacklist SET reason = %s, modify_date = %s " \
                                       "WHERE phone_num = %s"

        # 블랙리스트 삭제
        self.query_delete_black_list = "DELETE FROM b2c_blacklist WHERE phone_num = %s"

        # 블랙리스트 조회
        self.query_select_black_list = "SELECT * FROM b2c_blacklist WHERE phone_num = %s"

        # 블랙리스트 조회 전체
        self.query_select_black_list_all = "SELECT * FROM b2c_blacklist"

    def getBlackList(self, phone_num=None):
        print (phone_num)

        db = MysqlDatabase()
        if (phone_num == None):
            black = db.selectQuery(self.query_select_black_list_all)
        else:
            black = db.selectQuery(self.query_select_black_list, phone_num)

        return black



    def registBlackList(self, phone_num, reason, user_id):
        db = MysqlDatabase()
        db.executeQuery(self.query_insert_black_list, phone_num, reason, user_id, datetime.datetime.now(), datetime.datetime.now())


    def updateBlackList(self, phone_num, reason):
        db = MysqlDatabase()
        db.executeQuery(self.query_update_black_list, reason, datetime.datetime.now(), phone_num)


    def deleteBlackList(self, phone_num):
        print (phone_num)
        db = MysqlDatabase()
        db.executeQuery(self.query_delete_black_list, phone_num)
