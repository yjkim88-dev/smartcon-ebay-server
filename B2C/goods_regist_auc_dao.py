#_*_ coding: utf-8 _*_

from B2C.DataBase import MysqlDatabase
import datetime

class GoodsRegistAucDao:
    def __init__(self):
        # 옥션 상품등록
        self.query_insert_eventgoods = "INSERT INTO b2c_event_goods (svc_event_id, svc_goods_id, item_no)" \
                                       "VALUES (%s, %s, %s)"

        self.query_select_eventgoods = "SELECT * FROM b2c_event_goods WHERE item_no = %s "

        self.query_update_eventgoods = "UPDATE b2c_event_goods " \
                                  "SET svc_event_id = %s, svc_goods_id = %s, item_no = %s " \
                                  "WHERE item_no = %s"


    # 상품 이벤트 등록
    def insertEventGoods(self, event_id, goods_id, item_no):

        db = MysqlDatabase()
        row = db.selectQuery(self.query_select_eventgoods, item_no)

        if (len(row) > 0):
            db.executeQuery(self.query_update_eventgoods, event_id, goods_id, item_no)
        else:
            db.executeQuery(self.query_insert_eventgoods, event_id, goods_id, item_no)

