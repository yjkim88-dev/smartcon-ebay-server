#_*_ coding: utf-8 _*_

from B2C.DataBase import MysqlDatabase

class UserDao:
    def __init__(self):
        # 유저 정보 select
        self.query_select_user = "select * from b2c_admin_user where userid = %s"

        # 유저 토큰 update
        self.query_update_token = "update b2c_admin_user set auth_token = %s where userid = %s"

        # 유저 생성
        self.query_insert_user = "insert into b2c_admin_user (userid, password, auth_token, enc_key) values(%s, %s, %s, %s)"

    def selectUser(self, user_id):
        db = MysqlDatabase()
        user = db.selectQuery(self.query_select_user, user_id)

        return user

    def updateToken(self, token, userid):
        db = MysqlDatabase()
        db.executeQuery(self.query_update_token, token, userid)

    def insertUser(self, user_id, password, auth_token, enc_key):
        db = MysqlDatabase()
        db.executeQuery(self.query_insert_user, user_id, password, auth_token, enc_key)





