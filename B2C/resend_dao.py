#_*_ coding: utf-8 _*_

from B2C.DataBase import MysqlDatabase

class ResendDao:
    def __init__(self):
        # 재발송 로그 insert
        self.query_insert_resend_log = "INSERT INTO b2c_resend_log (event_id, barcode_num, buyer_mobile, receiver_mobile, " \
                                       "title, content, resend_count, resend_date, tr_id)" \
                                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        self.query_select_resend_log = "SELECT * FROM b2c_resend_log WHERE tr_id = %s "

    def selectResendLog(self, tr_id):
        db = MysqlDatabase()

        resends = db.selectQuery(self.query_select_resend_log, tr_id)

        return resends


    def insertResnedLog(self, evnet_id, barcode_num, buyer_mobile, receiver_mobile, title, content, resend_count,
                        resend_date, tr_id):

        db = MysqlDatabase()

        db.executeQuery(self.query_insert_resend_log, evnet_id, barcode_num, buyer_mobile, receiver_mobile, title, content,
                        resend_count, resend_date, tr_id)
