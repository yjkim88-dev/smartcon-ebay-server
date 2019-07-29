#_*_ coding: utf-8 _*_

from B2C.DataBase import MysqlDatabase

class CouponState:
    def __init__(self):
        # 조회
        self.query_coupon_state = "SELECT * FROM b2c_coupon_state WHERE tr_id = %s"


        # 쿠폰 상태 로그
        self.query_insert_coupon_state = "INSERT INTO b2c_coupon_state (send_no, order_id, tr_id, claim_type) "\
                                         "VALUES (%s, %s, %s, %s)"

        # 발송상태 업데이트
        self.query_update_send_log = "UPDATE b2c_coupon_state " \
                                     "SET send_status = %s, order_id = %s, sms_type = %s, sms_date = %s " \
                                     "WHERE tr_id = %s"
        # 교환상태 업데이트
        self.query_update_exchange = "UPDATE b2c_coupon_state " \
                                     "SET claim_type = %s, rcompany_name = %s, branch_name = %s, exchange_status = %s, valid_start = %s, valid_end = %s, claim_date = %s, exchange_date = %s " \
                                     "WHERE tr_id = %s"

        # 유효기간 종료일 업데이트
        self.query_update_exchange_end_date = "UPDATE b2c_coupon_state " \
                                              "SET valid_end = %s " \
                                              "WHERE tr_id = %s "

        # 주문 취소 아이디 업데이트
        self.query_update_cancel_user = "UPDATE b2c_coupon_state " \
                                              "SET cancel_user = %s " \
                                              "WHERE tr_id = %s "

    def selectCouponState(self, tr_id):
        db = MysqlDatabase()
        state = db.selectQuery(self.query_coupon_state, tr_id)

        return state

    def insertCouponState(self, send_no, order_id, tr_id):
        db = MysqlDatabase()
        db.executeQuery(self.query_insert_coupon_state, send_no, order_id, tr_id, 'N')


    def updateSendState(self, send_no, order_id, sms_status, sms_type, sms_date, tr_id):
        db = MysqlDatabase()

        states = self.selectCouponState(tr_id)

        if (len(states) == 0):
            db.executeQuery(self.query_insert_coupon_state, send_no, order_id, tr_id, 'N')

        print (sms_date)

        db.executeQuery(self.query_update_send_log, sms_status, order_id, sms_type, sms_date, tr_id)


    def updateEndDate(self, valid_end, tr_id):
        db = MysqlDatabase()
        db.executeQuery(self.query_update_exchange_end_date, valid_end, tr_id)

    def updateCancelUser(self, cancel_user, tr_id):
        db = MysqlDatabase()
        db.executeQuery(self.query_update_cancel_user, cancel_user, tr_id)

    def updateCouponState(self, send_no, order_id, claim_type, rcompany_name, branch_name, exchange_status, valid_start,
                          valid_end, claim_date, exchange_date, tr_id):
        db = MysqlDatabase()

        states = self.selectCouponState(tr_id)

        if (len(states) == 0):
            db.executeQuery(self.query_insert_coupon_state, send_no, order_id, tr_id, 'N')

        print ('--------valid--------')
        print (valid_start)
        print (valid_end)
        db.executeQuery(self.query_update_exchange, claim_type, rcompany_name, branch_name, exchange_status, valid_start,
                        valid_end, claim_date, exchange_date, tr_id)



