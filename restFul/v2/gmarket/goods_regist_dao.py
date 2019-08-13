#_*_ coding: utf-8 _*_

from B2C.DataBase import MysqlDatabase
import datetime
from Logger import Logger
from restFul.utils import Utils
from restFul.repository import StrRepository

class GoodsRegistDao:
    def __init__(self):
        # 지마켓 상품등록
        self.query_insert_goods = "INSERT INTO b2c_goods (create_date, modify_date, out_item_no, category_code, item_no, item_name," \
                                       "gd_html, maker_no, expiration_date, price, default_image, large_image, small_image," \
                                       "auto_term_duration, auto_use_term_duration, use_information, help_desk_telno, apply_place, apply_place_url, apply_place_telephone," \
                                       "display_date, stock_qty, regist_user, shipping_group_code)" \
                                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"


        # 조회
        self.query_select_goods_item_no = "SELECT * FROM b2c_goods WHERE " \
                                          "modify_date >= %s AND modify_date < %s " \
                                          "AND item_no = %s"

        self.query_select_goods_item_no2 = "SELECT * FROM b2c_goods WHERE item_no = %s"

        # 주문내역 조회
        self.query_select_goods = "SELECT * FROM b2c_goods WHERE " \
                                  "modify_date >= %s AND modify_date < %s "

        self.query_update_goods = "UPDATE b2c_goods " \
                                  "SET modify_date = %s, out_item_no = %s, category_code = %s, item_no = %s," \
                                          "item_name = %s, gd_html = %s, maker_no = %s, expiration_date = %s, price = %s," \
                                          "default_image = %s, large_image = %s, small_image = %s, auto_term_duration = %s," \
                                          "auto_use_term_duration = %s,"\
                                          "use_information = %s, help_desk_telno = %s, apply_place = %s, apply_place_url = %s," \
                                          "apply_place_telephone = %s, display_date = %s, stock_qty = %s, regist_user = %s, shipping_group_code = %s " \
                                  "WHERE item_no = %s"

        self.query_update_goods_coupon_info = "UPDATE b2c_goods" \
                                              "SET modify_date = %s, auto_term_duration = %s, auto_use_term_duration = %s" \
                                              "use_infomation = %s, help_desk_telno = %s, apply_place = %s, apply_place_url = %s" \
                                              "apply_place_telephone = %s "\
                                              "WHERE item_no = %s"

    def update_goods_coupon_info(self, coupon_info):
        Logger.logger.info('[0]Update goods coupon info start')

        coupon_info = coupon_info.add_item_coupon
        Logger.logger.info('[1]db connect')
        db = MysqlDatabase()
        goods = db.selectQuery(self.query_select_goods_item_no2, coupon_info.get('GmktItemNo'))
        Logger.logger.info('db connect success')

        Logger.logger.info(coupon_info)
        Logger.logger.info('[2]update')
        if(len(goods)>0):
            today = datetime.datetime.now()
            db.executeQuery(self.query_update_goods_coupon_info, today, coupon_info.get('AutoTermDuration'),
                            coupon_info.get('AutoUseTermDuration'), coupon_info.get('UseInformation'),
                            coupon_info.get('HelpDeskTelNo'), coupon_info.get('ApplyPlace'), coupon_info.get('ApplyPlaceUrl'),
                            coupon_info.get('ApplyPlaceTelephone'), coupon_info.get('GmktItemNo'))
        else:
            return Utils().makeResponse(StrRepository().error_coupon_regist)

        Logger.logger.info('[2]Update Goods Coupon Info Update Success')

    def insertGoods(self, item_no, add_item_model, user_id):
        Logger.logger.info('[0]insert goods start')

        db = MysqlDatabase()
        goods = db.selectQuery(self.query_select_goods_item_no2, item_no)
        Logger.logger.info('[1]db connection clear')
        today = datetime.datetime.now()
        print (len(goods))
        if (len(goods) > 0):
            Logger.logger.info('[2]update task...')
            print('update')
        else:
            Logger.logger.info('[2]insert task...')
            add_item = add_item_model.add_item
            reference_price = add_item_model.reference_price
            item_image = add_item_model.item_image
            shipping = add_item_model.shipping
            Logger.logger.info(add_item)
            Logger.logger.info(reference_price)
            Logger.logger.info(item_image)
            Logger.logger.info(shipping)
            #display_date=None, stock_qty=None,                                              # AddPrice
            #     regist_user=user_id, )

            # create_date, modify_date, out_item_no, category_code, item_no, item_name, " \
            # gd_html, maker_no, expiration_date, price, default_image, large_image, small_image, " \
            # auto_term_duration, auto_use_term_duration, use_information, help_desk_telno, apply_place, apply_place_url, apply_place_telephone, " \
            # display_date, stock_qty, regist_user, shipping_group_code
            db.executeQuery(self.query_insert_goods,
                            today, today, add_item.get('OutItemNo'), add_item.get('CategoryCode'), item_no,
                             add_item.get('ItemName'), add_item.get('GdHtml'), add_item.get('MakerNo'),
                             add_item.get('ExpirationDate'), reference_price.get('Price'), item_image.get('DefaultImage'),
                             item_image.get('LargeImage'), item_image.get('SmallImage'), None, None, None, None, None, None, None,
                             None, None, user_id, shipping.get('GroupCode')
                            )

    def selectGoods(self, start_date, end_date, item_no=None):
        db = MysqlDatabase()

        end_tmp = datetime.datetime.strptime(end_date, '%Y%m%d')
        end_tmp = end_tmp + datetime.timedelta(days=1)
        end_date = end_tmp.strftime('%Y%m%d')

        if (item_no != None and item_no != ''):
            return db.selectQuery(self.query_select_goods_item_no, start_date, end_date, item_no)
        else:
            return db.selectQuery(self.query_select_goods, start_date, end_date)
