#_*_ coding: utf-8 _*_

from B2C.DataBase import MysqlDatabase
import datetime

class OrderListDao:
    def __init__(self):
        # 주문내역 조회
        self.query_select_order_list = "SELECT * FROM b2c_order " \
                                        "WHERE create_date >= %s " \
                                        "AND create_date < %s" \

        self.query_select_order_list_order_no = "SELECT * FROM b2c_order " \
                                               "WHERE order_no = %s "

        self.query_select_order_list_item_no = "SELECT * FROM b2c_order " \
                                                "WHERE item_no = %s "

        self.query_select_order_list_item_name = "SELECT * FROM b2c_order " \
                                                "WHERE item_name = %s "

        self.query_select_order_list_chanal = "SELECT * FROM b2c_order " \
                                                "WHERE member_id = %s "

        self.query_select_order_list_buyer = "SELECT * FROM b2c_order " \
                                                "WHERE buyer_mobile = %s "

        self.query_select_order_list_receiver = "SELECT * FROM b2c_order " \
                                                "WHERE receiver_mobile >= %s "

        self.query_select_order_list_goods_item = "SELECT * FROM b2c_order " \
                                                "WHERE out_item_no = %s "

        # 바코드 조회
        self.query_select_order_list_barcode = "SELECT * FROM b2c_order " \
                                               "WHERE order_no = (SELECT order_no FROM b2c_cpcre_log WHERE SVC_BARCODE_NUM = %s) "

        # 주문내역 조회
        # self.query_select_order_list = "SELECT * FROM b2c_order " \
        #                                "WHERE " \
        #                                "b2c_order.send_request_date BETWEEN STR_TO_DATE(%s, %s) AND STR_TO_DATE(%s, %s)"

        # 재발송 횟수 조회
        self.query_select_resend_count = "SELECT resend_count FROM b2c_send_log "\
                                         "WHERE svc_barcode_num = %s"

        # 재발송 횟수 업데이트
        self.query_update_resend_count = "UPDATE  b2c_send_log SET resend_count = %s " \
                                         "WHERE svc_barcode_num = %s"

        # 주문내역 insert
        self.query_insert_order = "INSERT INTO b2c_order (order_no, send_no, order_state, item_count, item_name, item_no, " \
                                                            "buyer_id, buyer_name, buyer_mobile, receiver_name, receiver_mobile, " \
                                                            "payment_date, send_request_date, create_date, member_id, out_item_no) " \
                                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"


    def insertOrder(self, order_no, send_no, order_state, item_count, item_name, item_no, buyer_id, buyer_name, buyer_mobile, receiver_name,
                                           receiver_mobile, payment_date, send_request_date, create_date, member_id, out_item_no):
        db = MysqlDatabase()
        db.executeQuery(self.query_insert_order, order_no, send_no, order_state, item_count, item_name, item_no, buyer_id, buyer_name, buyer_mobile, receiver_name,
                                           receiver_mobile, payment_date, send_request_date, create_date, member_id, out_item_no)



    def getOrderList(self, start_date, end_date, param_data_select, param_search_text):
        db = MysqlDatabase()

        end_tmp = datetime.datetime.strptime(end_date, '%Y%m%d')
        end_tmp = end_tmp + datetime.timedelta(days=1)
        end_date = end_tmp.strftime('%Y%m%d')

        if (param_data_select == 'option1'):
            order_list = db.selectQuery(self.query_select_order_list_order_no, param_search_text)
        elif (param_data_select == 'option2'):
            order_list = db.selectQuery(self.query_select_order_list_item_no, param_search_text)
        elif (param_data_select == 'option3'):
            order_list = db.selectQuery(self.query_select_order_list_item_name, param_search_text)
        elif (param_data_select == 'option4'):
            order_list = db.selectQuery(self.query_select_order_list_chanal, param_search_text)
        elif (param_data_select == 'option5'):
            order_list = db.selectQuery(self.query_select_order_list_buyer, param_search_text)
        elif (param_data_select == 'option6'):
            order_list = db.selectQuery(self.query_select_order_list_receiver, param_search_text)
        elif (param_data_select == 'option7'):
            order_list = db.selectQuery(self.query_select_order_list_goods_item, param_search_text)
        elif (param_data_select == 'option8'):
            order_list = db.selectQuery(self.query_select_order_list_barcode, param_search_text)
        else:
            order_list = db.selectQuery(self.query_select_order_list, start_date, end_date)

        return order_list


    def getReSendCount(self, barcode_num):
        db = MysqlDatabase()
        count = db.selectQuery(self.query_select_resend_count, barcode_num)

        return count

    def setReSendCount(self, barcode_num, count):
        db = MysqlDatabase()
        db.executeQuery(self.query_update_resend_count, count, barcode_num)





