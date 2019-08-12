#_*_ coding: utf-8 _*_

from B2C.DataBase import MysqlDatabase
import datetime

class GoodsRegistDao:
    def __init__(self):
        # 지마켓 상품등록
        self.query_insert_goods = "INSERT INTO b2c_goods (create_date, modify_date, out_item_no, category_code, item_no, item_name," \
                                       "gd_html, maker_no, expiration_date, price, default_image, large_image, small_image," \
                                       "auto_term_duration, auto_use_term_duration, use_information, help_desk_telno, apply_place, apply_place_url, apply_place_telephone," \
                                       "display_date, stock_qty, regist_user, shipping_group_code)" \
                                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        self.insert_goods_query = "INSERT INTO b2c_goods (create_date, modify_date, out_item_no, category_code, " \
                                  "item_no, item_name, gd_html, maker_no, expiration_date, price, default_image, " \
                                  "large_image, small_image, auto_term_duration, auto_use_term_duration, " \
                                  "use_information, help_desk_telno, apply_place, apply_place_url," \
                                  "apply_place_telephone, display_date, stock_qty, regist_user, shipping_group_code)" \
                                  "VALUES ({create_date}, {modify_date}, {out_item_no}, {category_code},{item_no}, " \
                                  "{item_name}, {gd_html}, {maker_no}, {expiration_date}, {price}, {default_image}, " \
                                  "{large_image}, {small_image}, {auto_term_duration}, {auto_use_term_duration}, " \
                                  "{use_infomation}, {help_desk_telno}, {apply_place}, {apply_place_url}, " \
                                  "{apply_place_telephone}, {display_date}, {stock_qty}, {regist_user}, " \
                                  "{shipping_group_code})"
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
        
    def insertGoods(self, item_no, add_item_model, user_id):

        db = MysqlDatabase()
        goods = db.selectQuery(self.query_select_goods_item_no2, item_no)

        today = datetime.datetime.now()

        print (len(goods))

        if (len(goods) > 0):
            print('update')
        else:
            add_item = add_item_model.add_item
            reference_price = add_item_model.reference_price
            item_image = add_item_model.item_image
            shipping = add_item_model.shipping

            query = self.insert_goods_query.format(
                create_date= today, modify_date= today, out_item_no=add_item.get('OutItemNo'),                                #AddItem
                category_code=add_item.get('CategoryCode'), item_no=item_no, item_name = add_item.get('ItemName'),
                gd_html= add_item.get('GdHtml'), maker_no= add_item.get('MakerNo'),
                expiration_date= add_item.get('ExpirationDate'), price= reference_price.get('Price'),
                default_image= item_image.get('DefaultImage'), large_image=item_image.get('LargeImage'),
                small_image= item_image.get('SmallImage'), shipping_group_code = shipping.get('GroupCode') ,
                auto_term_duration=None , use_infomation=None, help_desk_telno=None, apply_place=None, apply_place_url=None,  # AddItemCoupon
                apply_place_telephone=None, display_date=None, stock_qty=None,                                                # AddPrice
                regist_user=user_id, )
            db.executeQuery(query)

    def selectGoods(self, start_date, end_date, item_no=None):
        db = MysqlDatabase()

        end_tmp = datetime.datetime.strptime(end_date, '%Y%m%d')
        end_tmp = end_tmp + datetime.timedelta(days=1)
        end_date = end_tmp.strftime('%Y%m%d')

        if (item_no != None and item_no != ''):
            return db.selectQuery(self.query_select_goods_item_no, start_date, end_date, item_no)
        else:
            return db.selectQuery(self.query_select_goods, start_date, end_date)
