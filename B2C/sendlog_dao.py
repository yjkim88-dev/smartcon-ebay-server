#_*_ coding: utf-8 _*_

from B2C.DataBase import MysqlDatabase
import datetime

class SendLogDao:
    def __init__(self):
        # 발송 로그 select
        self.query_select_send = "SELECT * FROM b2c_send_log WHERE tr_id = %s "

        self.query_select_order_num = "SELECT * FROM b2c_send_log WHERE order_no = %s "

        # 재발송 횟수 업데이트
        self.query_update_resend_count = "UPDATE  b2c_send_log SET resend_count = %s " \
                                         "WHERE svc_barcode_num = %s"

        # 발송 결과 insert
        self.query_insert_send_result = "INSERT INTO b2c_send_log (order_no, send_no, svc_mms_result_code, svc_mms_result_msg, " \
                                        "svc_mms_date, svc_barcode_num, receiver_phone, buyer_phone, event_id, tr_id, member_id)" \
                                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        # 바코드 검색
        self.query_select_barcode = "SELECT * FROM b2c_send_log WHERE svc_barcode_num = %s "

        # 재발송 후 수신자 번호 업데이트
        self.query_update_receiver_mobile = "UPDATE b2c_send_log SET receiver_phone = %s " \
                                            "WHERE tr_id = %s "


    def insertSendLog(self, order_no, send_no, svc_mms_result_code, svc_mms_result_msg, svc_mms_date,
                        svc_barcode_num, receiver_phone, buyer_phone, event_id, tr_id, member_id):
        db = MysqlDatabase()
        db.executeQuery(self.query_insert_send_result, order_no, send_no, svc_mms_result_code, svc_mms_result_msg,
                        svc_mms_date, svc_barcode_num, receiver_phone, buyer_phone, event_id, tr_id, member_id)


    def selectSendLog(self, tr_id):
        db = MysqlDatabase()
        send_logs = db.selectQuery(self.query_select_send, tr_id)

        return send_logs

    def selectSendLogSendNom(self, order_no, param_data_select, param_search_text):
        db = MysqlDatabase()

        if (param_data_select == 'option8'):
            send_logs = db.selectQuery(self.query_select_barcode, param_search_text)
        else:
            send_logs = db.selectQuery(self.query_select_order_num, order_no)

        return send_logs

    def setResendCount(self, barcode_num, count):
        db = MysqlDatabase()
        db.executeQuery(self.query_update_resend_count, count, barcode_num)

    def updateReceiverMobile(self, receiver_phone, tr_id):
        db = MysqlDatabase()
        db.executeQuery(self.query_update_receiver_mobile, receiver_phone, tr_id)





