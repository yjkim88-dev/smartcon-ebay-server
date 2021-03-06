# _*_ coding: utf-8 _*_

from B2C.DataBase import MysqlDatabase
import datetime
from Logger import Logger
from restFul.utils import Utils
from restFul.repository import StrRepository


class GoodsRegistDao:
    def __init__(self):
        self.query_insert_goods_sub_init = "INSERT INTO b2c_goods_sub (item_no) VALUES (%s)"
        # 상품(마켓) 등록
        self.query_insert_goods = "INSERT INTO b2c_goods (create_date, modify_date, out_item_no, category_code, item_no, item_name," \
                                  "gd_html, maker_no, expiration_date, price, default_image, large_image, small_image," \
                                  "auto_term_duration, auto_use_term_duration, use_information, help_desk_telno, apply_place, apply_place_url, apply_place_telephone," \
                                  "display_date, stock_qty, regist_user, shipping_group_code)" \
                                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # 상품(마켓) sub 등록
        self.query_insert_sub_goods = "INSERT INTO b2c_goods_sub " \
                                      "(item_no, order_limit_max, order_limit_period, order_limit_count) " \
                                      "VALUES (%s, %s, %s, %s)"

        # sub 테이블 조회
        self.query_select_goods_sub_item_no = "SELECT * FROM b2c_goods_sub WHERE item_no = %s"

        # 상품들 조회
        self.query_select_goods_item_no = "SELECT * FROM b2c_goods WHERE " \
                                          "modify_date >= %s AND modify_date < %s " \
                                          "AND item_no = %s"
        # 고시정보 입력

        # 상품 조회
        self.query_select_goods_item_no2 = "SELECT * FROM b2c_goods WHERE item_no = %s"

        # 상품 조회 v3
        self.query_select_goods_item_no_v3 = "SELECT * FROM b2c_goods " \
                                             "LEFT OUTER JOIN b2c_goods_sub " \
                                             "ON b2c_goods.ITEM_NO = b2c_goods_sub.ITEM_NO " \
                                             "WHERE b2c_goods.ITEM_NO = %s"

        # 상품들 조회
        self.query_select_goods_item_list = "SELECT * FROM b2c_goods " \
                                            "LEFT OUTER JOIN b2c_goods_sub " \
                                            "ON b2c_goods.ITEM_NO = b2c_goods_sub.ITEM_NO "

        # 주문내역 조회
        self.query_select_goods = "SELECT * FROM b2c_goods WHERE " \
                                  "modify_date >= %s AND modify_date < %s " \
                                  "ORDER BY modify_date DESC"

        # 고시정보 업데이트
        self.query_update_sub_goods_ofiicial_info = "UPDATE b2c_goods_sub " \
                                                    "SET issuer= %s, OFFICIAL_EXPRIATION_DATE_OR_USE_CONDITION = %s, use_brand = %s, " \
                                                    "refund_condition_and_rule = %s, counsel_tel_no=%s " \
                                                    "WHERE item_no = %s"

        # 상품(마켓) 정보 업데이트
        self.query_update_goods_market_info = "UPDATE b2c_goods " \
                                              "SET modify_date = %s, out_item_no = %s, category_code = %s, item_no = %s," \
                                              "item_name = %s, gd_html = %s, maker_no = %s, expiration_date = %s, price = %s," \
                                              "default_image = %s, large_image = %s, small_image = %s," \
                                              "regist_user = %s, shipping_group_code = %s " \
                                              "WHERE item_no = %s"

        # 상품(마켓)정보 업데이트2
        self.query_update_goods_market_info_v2 = "UPDATE b2c_goods INNER JOIN b2c_goods_sub " \
                                                 "ON b2c_goods.item_no = b2c_goods_sub.item_no " \
                                                 "SET b2c_goods.modify_date = %s, b2c_goods.out_item_no = %s, " \
                                                 "b2c_goods.category_code = %s, b2c_goods.item_no = %s," \
                                                 "b2c_goods.item_name = %s, b2c_goods.gd_html = %s, b2c_goods.maker_no = %s, " \
                                                 "b2c_goods.expiration_date = %s, b2c_goods.price = %s," \
                                                 "b2c_goods.default_image = %s, b2c_goods.large_image = %s, " \
                                                 "b2c_goods.small_image = %s, b2c_goods.regist_user = %s, " \
                                                 "b2c_goods.shipping_group_code = %s, " \
                                                 "b2c_goods_sub.order_limit_max = %s, b2c_goods_sub.order_limit_period=%s," \
                                                 "b2c_goods_sub.order_limit_count = %s " \
                                                 "WHERE b2c_goods.item_no = %s"
        # 쿠폰 정보(쿠폰마켓) 업데이트
        self.query_update_goods_coupon_info = "UPDATE b2c_goods " \
                                              "SET modify_date = %s, auto_term_duration = %s, auto_use_term_duration = %s, " \
                                              "use_information = %s, help_desk_telno = %s, apply_place = %s, apply_place_url = %s, " \
                                              "apply_place_telephone = %s " \
                                              "WHERE item_no = %s"

        # 쿠폰 정보 업데이트 v2
        self.query_update_goods_coupon_info_v2 = "UPDATE b2c_goods INNER JOIN b2c_goods_sub " \
                                                 "ON b2c_goods.item_no = b2c_goods_sub.item_no " \
                                                 "SET b2c_goods.modify_date = %s, b2c_goods.auto_term_duration = %s, " \
                                                 "b2c_goods.auto_use_term_duration = %s, b2c_goods.use_information = %s, " \
                                                 "b2c_goods.help_desk_telno = %s, b2c_goods.apply_place = %s, " \
                                                 "b2c_goods.apply_place_url = %s, b2c_goods.apply_place_telephone = %s, " \
                                                 "b2c_goods_sub.service_name = %s, b2c_goods_sub.valid_term_type = %s," \
                                                 "b2c_goods_sub.auto_term_start_day = %s, b2c_goods_sub.fixed_term_start_date= %s," \
                                                 "b2c_goods_sub.fixed_term_end_date =%s, b2c_goods_sub.use_term_type =%s," \
                                                 "b2c_goods_sub.auto_use_term_start_day =%s, b2c_goods_sub.fixed_use_term_start_date=%s," \
                                                 "b2c_goods_sub.fixed_use_term_end_date=%s, b2c_goods_sub.find_guide=%s," \
                                                 "b2c_goods_sub.publication_corp=%s, publication_corp_web_url=%s," \
                                                 "b2c_goods_sub.is_cancel=%s, b2c_goods_sub.coupon_image_url = %s " \
                                                 "WHERE b2c_goods.item_no = %s"

        # 가격 정보 업데이트
        self.query_update_goods_price_info = "UPDATE b2c_goods " \
                                             "SET modify_date = %s, display_date = %s, stock_qty = %s " \
                                             "WHERE item_no = %s"

    def upload_scms_data(self, params):
        # 상품(마켓)정보 업데이트2

        db = MysqlDatabase()
        goods = db.selectQuery(self.query_select_goods_item_no2, params.get('ITEM_NO'))

        if (len(goods) > 0):
            pass
        else:
            db.executeQuery(
                self.query_insert_goods,
                params.get('CREATE_DATE'), params.get('MODIFY_DATE'), params.get('OUT_ITEM_NO'),
                params.get('CAEGORY_CODE'),
                params.get('ITEM_NO'), params.get("ITEM_NAME"), params.get("GD_HTML"), params.get("MAKER_NO"),
                params.get("EXPIRATION_DATE"), params.get("PRICE"), params.get("DEFAULT_IMAGE"),
                params.get("LARGE_IMAGE"),
                params.get("SMALL_IMAGE"), params.get("AUTO_TERM_DURATION"), params.get("AUTO_USE_TERM_DURATION"),
                params.get("USE_INFORMATION"), params.get("HELP_DESK_TELNO"),
                params.get("APPLY_PLACE"), params.get("APPLY_PLACE_URL"), params.get("APPLY_PLACE_TELEPHONE"),
                params.get("DISPLAY_DATE"),
                params.get("STOCK_QTY"), params.get("REGIST_USER"), params.get("SHIPPING_GROUP_CODE"),
            )

            db.executeQuery(
                self.query_insert_sub_goods, params.get('ITEM_NO'), params.get('OrderLimitMax'),
                params.get('OrderLimitPeriod'), params.get('OrderLimitCount')
            )
        return 1

    def fetch_goods(self, item_no):
        try:
            Logger.logger.info('===== fetchGoods STEP1 DB Connection =====')
            db = MysqlDatabase()
            Logger.logger.info('===== fetchGoods DB Connection Complete=====')

            Logger.logger.info('===== fetchGoods STEP2 Fetch Goods =====')

            sub_goods = db.selectQuery(self.query_select_goods_sub_item_no, item_no)
            if len(sub_goods) < 0:
                db.executeQuery(self.query_insert_goods_sub_init, item_no)

            goods = db.selectQuery(self.query_select_goods_item_no_v3, item_no)
            Logger.logger.info('===== fetchGoods Fetch Goods Complete=====')
            goods = goods[0]
            goods = {
                'price': goods['PRICE'],
                'create_date': str(goods['CREATE_DATE']) if goods['CREATE_DATE'] is not None else None,
                'modify_date': str(goods['MODIFY_DATE']) if goods['MODIFY_DATE'] is not None else None,
                'use_information': goods['USE_INFORMATION'],
                'auto_term_duration': goods['AUTO_TERM_DURATION'],
                'help_desk_telno': goods['HELP_DESK_TELNO'],
                'large_image': goods['LARGE_IMAGE'],
                'small_image': goods['SMALL_IMAGE'],
                'default_image': goods['DEFAULT_IMAGE'],
                'shipping_group_code': goods['SHIPPING_GROUP_CODE'],
                'expiration_date': str(goods['EXPIRATION_DATE']) if goods['EXPIRATION_DATE'] is not None else None,
                'apply_place': goods['APPLY_PLACE'],
                'item_no': goods['ITEM_NO'],
                'stock_qty': goods['STOCK_QTY'],
                'item_name': goods['ITEM_NAME'],
                'apply_place_telephone': goods['APPLY_PLACE_TELEPHONE'],
                'gd_html': goods['GD_HTML'],
                'out_item_no': goods['OUT_ITEM_NO'],
                'maker_no': goods['MAKER_NO'],
                'display_date': str(goods['DISPLAY_DATE']) if goods['DISPLAY_DATE'] is not None else None,
                'apply_place_url': goods['APPLY_PLACE_URL'],
                'auto_use_term_duration': goods['AUTO_USE_TERM_DURATION'],
                'category_code': goods['CATEGORY_CODE'],
                'order_limit_max': goods['ORDER_LIMIT_MAX'],  # goods_sub
                'order_limit_period': goods['ORDER_LIMIT_PERIOD'],
                'order_limit_count': goods['ORDER_LIMIT_COUNT'],
                'issuer': goods['ISSUER'],
                'official_expiration_date_or_use_condition': goods['OFFICIAL_EXPRIATION_DATE_OR_USE_CONDITION'],
                'use_brand': goods['USE_BRAND'],
                'refund_condition_and_rule': goods['REFUND_CONDITION_AND_RULE'],
                'counsel_tel_no': goods['COUNSEL_TEL_NO'],
                'service_name': goods['SERVICE_NAME'],
                'valid_term_type': goods['VALID_TERM_TYPE'],
                'auto_term_start_day': goods['AUTO_TERM_START_DAY'],
                'fixed_term_start_date': str(goods['FIXED_TERM_START_DATE']) if goods[
                                                                                    'FIXED_TERM_START_DATE'] is not None else None,
                'fixed_term_end_date': str(goods['FIXED_TERM_END_DATE']) if goods[
                                                                                'FIXED_TERM_END_DATE'] is not None else None,
                'use_term_type': goods['USE_TERM_TYPE'],
                'auto_use_term_start_day': goods['AUTO_USE_TERM_START_DAY'],
                'fixed_use_term_start_date': str(goods['FIXED_USE_TERM_START_DATE']) if goods[
                                                                                            'FIXED_USE_TERM_START_DATE'] is not None else None,
                'fixed_use_term_end_date': str(goods['FIXED_USE_TERM_END_DATE']) if goods[
                                                                                        'FIXED_USE_TERM_END_DATE'] is not None else None,
                'find_guide': goods['FIND_GUIDE'],
                'publication_corp': goods['PUBLICATION_CORP'],
                'publication_corp_web_url': goods['PUBLICATION_CORP_WEB_URL'],
                'is_cancel': goods['IS_CANCEL'],
                'coupon_image_url': goods['COUPON_IMAGE_URL'],
            }
        except BaseException as e:
            Logger.logger.info('===== fetchGoods Faild =====')
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)
        return Utils().makeResponse(StrRepository().error_none, goods)

    def fetch_official_info_goods(self):
        try:
            goods_list = []
            Logger.logger.info('===== fetchGoodsOfficialInfo STEP1 DB Connection =====')
            db = MysqlDatabase()
            Logger.logger.info('===== fetchGoodsOfficialInfo DB Connection Complete=====')

            Logger.logger.info('===== fetchGoodsOfficialInfo STEP2 Fetch GoodsList =====')

            mysql_goods_list = db.selectQuery(self.query_select_goods_item_list)
            Logger.logger.info('===== fetchGoodsOfficialInfo Fetch GoodsList Complete=====')
            for goods in mysql_goods_list:
                goods_tmp = {
                    'item_no': goods['ITEM_NO'],
                    'issuer': goods['ISSUER'] if goods['ISSUER'] is not None else '(주) 스마트콘',
                    'official_expiration_date_or_use_condition': goods['OFFICIAL_EXPRIATION_DATE_OR_USE_CONDITION'],
                    'use_brand': goods['USE_BRAND'],
                    'refund_condition_and_rule': goods['REFUND_CONDITION_AND_RULE'],
                    'counsel_tel_no': goods['COUNSEL_TEL_NO'],
                }
                goods_list.append(goods_tmp)

        except BaseException as e:
            Logger.logger.info('===== fetchGoodsOfficialInfo Faild =====')
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)
        return Utils().makeResponse(StrRepository().error_none, goods_list)

    def fetch_goods_list_coupon(self):
        try:
            goods_list = []
            Logger.logger.info('===== fetchGoods STEP1 DB Connection =====')
            db = MysqlDatabase()
            Logger.logger.info('===== fetchGoods DB Connection Complete=====')

            Logger.logger.info('===== fetchGoods STEP2 Fetch Goods =====')
            mysql_goods_list = db.selectQuery(self.query_select_goods_item_list)
            Logger.logger.info('===== fetchGoods Fetch Goods Complete=====')
            for goods in mysql_goods_list:
                goods_tmp = {
                    'price': goods['PRICE'],
                    'create_date': str(goods['CREATE_DATE']) if goods['CREATE_DATE'] is not None else None,
                    'modify_date': str(goods['MODIFY_DATE']) if goods['MODIFY_DATE'] is not None else None,
                    'use_information': goods['USE_INFORMATION'],
                    'auto_term_duration': goods['AUTO_TERM_DURATION'],
                    'help_desk_telno': goods['HELP_DESK_TELNO'],
                    'large_image': goods['LARGE_IMAGE'],
                    'small_image': goods['SMALL_IMAGE'],
                    'default_image': goods['DEFAULT_IMAGE'],
                    'shipping_group_code': goods['SHIPPING_GROUP_CODE'],
                    'expiration_date': str(goods['EXPIRATION_DATE']) if goods['EXPIRATION_DATE'] is not None else None,
                    'apply_place': goods['APPLY_PLACE'],
                    'item_no': goods['ITEM_NO'],
                    'stock_qty': goods['STOCK_QTY'],
                    'item_name': goods['ITEM_NAME'],
                    'apply_place_telephone': goods['APPLY_PLACE_TELEPHONE'],
                    'gd_html': goods['GD_HTML'],
                    'out_item_no': goods['OUT_ITEM_NO'],
                    'maker_no': goods['MAKER_NO'],
                    'display_date': str(goods['DISPLAY_DATE']) if goods['DISPLAY_DATE'] is not None else None,
                    'apply_place_url': goods['APPLY_PLACE_URL'],
                    'auto_use_term_duration': goods['AUTO_USE_TERM_DURATION'],
                    'category_code': goods['CATEGORY_CODE'],
                    'order_limit_max': goods['ORDER_LIMIT_MAX'],  # goods_sub
                    'order_limit_period': goods['ORDER_LIMIT_PERIOD'],
                    'order_limit_count': goods['ORDER_LIMIT_COUNT'],
                    'issuer': goods['ISSUER'],
                    'official_expiration_date_or_use_condition': goods['OFFICIAL_EXPRIATION_DATE_OR_USE_CONDITION'],
                    'use_brand': goods['USE_BRAND'],
                    'refund_condition_and_rule': goods['REFUND_CONDITION_AND_RULE'],
                    'counsel_tel_no': goods['COUNSEL_TEL_NO'],
                    'service_name': goods['SERVICE_NAME'],
                    'valid_term_type': goods.get('VALID_TERM_TYPE') if goods['VALID_TERM_TYPE'] is not None else 'AutoTerm',
                    'auto_term_start_day': goods.get('AUTO_TERM_START_DAY') if goods['AUTO_TERM_START_DAY'] is not None else '0',
                    'fixed_term_start_date': str(goods['FIXED_TERM_START_DATE']) if goods[
                                                                                        'FIXED_TERM_START_DATE'] is not None else None,
                    'fixed_term_end_date': str(goods['FIXED_TERM_END_DATE']) if goods[
                                                                                    'FIXED_TERM_END_DATE'] is not None else None,
                    'use_term_type': goods.get('USE_TERM_TYPE') if goods['USE_TERM_TYPE'] is not None else 'AutoTerm',
                    'auto_use_term_start_day': goods.get('AUTO_USE_TERM_START_DAY') if goods['AUTO_USE_TERM_START_DAY'] is not None else '0',
                    'fixed_use_term_start_date': str(goods['FIXED_USE_TERM_START_DATE']) if goods[
                                                                                                'FIXED_USE_TERM_START_DATE'] is not None else None,
                    'fixed_use_term_end_date': str(goods['FIXED_USE_TERM_END_DATE']) if goods[
                                                                                            'FIXED_USE_TERM_END_DATE'] is not None else None,
                    'find_guide': goods['FIND_GUIDE'],
                    'publication_corp': goods.get('PUBLICATION_CORP') if goods['PUBLICATION_CORP'] is not None else "(주) 스마트콘",
                    'publication_corp_web_url': goods.get('PUBLICATION_CORP_WEB_URL') if goods.get('PUBLICATION_CORP_WEB_URL') is not None else "http://www.smartconcorp.com/",
                    'is_cancel': goods['IS_CANCEL'],
                    'coupon_image_url': goods['COUPON_IMAGE_URL'],
                }
                goods_list.append(goods_tmp)
        except BaseException as e:
            Logger.logger.info('===== fetchGoods Faild =====')
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)
        return Utils().makeResponse(StrRepository().error_none, goods_list)

    def fetch_goods_list(self,start_date, end_date):
        try:
            goods_list = []
            Logger.logger.info('===== fetchGoods STEP1 DB Connection =====')
            db = MysqlDatabase()
            Logger.logger.info('===== fetchGoods DB Connection Complete=====')

            Logger.logger.info('===== fetchGoods STEP2 Fetch Goods =====')
            mysql_goods_list = db.selectQuery(self.query_select_goods_item_list)
            Logger.logger.info('===== fetchGoods Fetch Goods Complete=====')
            for goods in mysql_goods_list:
                goods_tmp = {
                    'price': goods['PRICE'],
                    'create_date': str(goods['CREATE_DATE']) if goods['CREATE_DATE'] is not None else None,
                    'modify_date': str(goods['MODIFY_DATE']) if goods['MODIFY_DATE'] is not None else None,
                    'use_information': goods['USE_INFORMATION'],
                    'auto_term_duration': goods['AUTO_TERM_DURATION'],
                    'help_desk_telno': goods['HELP_DESK_TELNO'],
                    'large_image': goods['LARGE_IMAGE'],
                    'small_image': goods['SMALL_IMAGE'],
                    'default_image': goods['DEFAULT_IMAGE'],
                    'shipping_group_code': goods['SHIPPING_GROUP_CODE'],
                    'expiration_date': str(goods['EXPIRATION_DATE']) if goods['EXPIRATION_DATE'] is not None else None,
                    'apply_place': goods['APPLY_PLACE'],
                    'item_no': goods['ITEM_NO'],
                    'stock_qty': goods['STOCK_QTY'],
                    'item_name': goods['ITEM_NAME'],
                    'apply_place_telephone': goods['APPLY_PLACE_TELEPHONE'],
                    'gd_html': goods['GD_HTML'],
                    'out_item_no': goods['OUT_ITEM_NO'],
                    'maker_no': goods['MAKER_NO'],
                    'display_date': str(goods['DISPLAY_DATE']) if goods['DISPLAY_DATE'] is not None else None,
                    'apply_place_url': goods['APPLY_PLACE_URL'],
                    'auto_use_term_duration': goods['AUTO_USE_TERM_DURATION'],
                    'category_code': goods['CATEGORY_CODE'],
                    'order_limit_max': goods['ORDER_LIMIT_MAX'],  # goods_sub
                    'order_limit_period': goods['ORDER_LIMIT_PERIOD'],
                    'order_limit_count': goods['ORDER_LIMIT_COUNT'],
                    'issuer': goods['ISSUER'],
                    'official_expiration_date_or_use_condition': goods['OFFICIAL_EXPRIATION_DATE_OR_USE_CONDITION'],
                    'use_brand': goods['USE_BRAND'],
                    'refund_condition_and_rule': goods['REFUND_CONDITION_AND_RULE'],
                    'counsel_tel_no': goods['COUNSEL_TEL_NO'],
                    'service_name': goods['SERVICE_NAME'],
                    'valid_term_type': goods['VALID_TERM_TYPE'],
                    'auto_term_start_day': goods['AUTO_TERM_START_DAY'],
                    'fixed_term_start_date': str(goods['FIXED_TERM_START_DATE']) if goods[
                                                                                        'FIXED_TERM_START_DATE'] is not None else None,
                    'fixed_term_end_date': str(goods['FIXED_TERM_END_DATE']) if goods[
                                                                                    'FIXED_TERM_END_DATE'] is not None else None,
                    'use_term_type': goods['USE_TERM_TYPE'],
                    'auto_use_term_start_day': goods['AUTO_USE_TERM_START_DAY'],
                    'fixed_use_term_start_date': str(goods['FIXED_USE_TERM_START_DATE']) if goods[
                                                                                                'FIXED_USE_TERM_START_DATE'] is not None else None,
                    'fixed_use_term_end_date': str(goods['FIXED_USE_TERM_END_DATE']) if goods[
                                                                                            'FIXED_USE_TERM_END_DATE'] is not None else None,
                    'find_guide': goods['FIND_GUIDE'],
                    'publication_corp': goods['PUBLICATION_CORP'],
                    'publication_corp_web_url': goods['PUBLICATION_CORP_WEB_URL'],
                    'is_cancel': goods['IS_CANCEL'],
                    'coupon_image_url': goods['COUPON_IMAGE_URL'],
                }
                goods_list.append(goods_tmp)
        except BaseException as e:
            Logger.logger.info('===== fetchGoods Faild =====')
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)
        return Utils().makeResponse(StrRepository().error_none, goods_list)

    def goods_market_info_db_service(self, item_no, add_item_model, user_id):
        Logger.logger.info('[0]insert goods start')
        db = MysqlDatabase()
        goods = db.selectQuery(self.query_select_goods_item_no2, item_no)
        Logger.logger.info('[1]db connection clear')
        today = datetime.datetime.now()

        add_item = add_item_model.add_item
        reference_price = add_item_model.reference_price
        order_limit = add_item_model.order_limit
        item_image = add_item_model.item_image
        shipping = add_item_model.shipping

        if (len(goods) > 0):
            sub_goods = db.selectQuery(self.query_select_goods_sub_item_no, item_no)
            if len(sub_goods) < 0:
                db.executeQuery(self.query_insert_goods_sub_init, item_no)
            Logger.logger.info('[2]update task...')
            db.executeQuery(
                self.query_update_goods_market_info_v2,
                today, add_item.get('OutItemNo'), add_item.get('CategoryCode'), item_no,
                add_item.get('ItemName'), add_item.get('GdHtml'), add_item.get('MakerNo'),
                add_item.get('ExpirationDate'), reference_price.get('Price'),
                item_image.get('DefaultImage'), item_image.get('LargeImage'), item_image.get('SmallImage'),
                user_id, shipping.get('GroupCode'), order_limit.get('OrderLimitMax'),
                order_limit.get('OrderLimitPeriod'), order_limit.get('OrderLimitCount'),
                item_no
            )
        else:
            Logger.logger.info('[2]insert task...')
            db.executeQuery(
                self.query_insert_goods,
                today, today, add_item.get('OutItemNo'), add_item.get('CategoryCode'), item_no,
                add_item.get('ItemName'), add_item.get('GdHtml'), add_item.get('MakerNo'),
                add_item.get('ExpirationDate'), reference_price.get('Price'),
                item_image.get('DefaultImage'),
                item_image.get('LargeImage'), item_image.get('SmallImage'), None, None, None, None, None,
                None, None, None, None, user_id, shipping.get('GroupCode')
            )
            db.executeQuery(
                self.query_insert_sub_goods, item_no, order_limit.get('OrderLimitMax'),
                order_limit.get('OrderLimitPeriod'), order_limit.get('OrderLimitCount')
            )
        return Utils().makeResponse(StrRepository().error_none)

    def update_goods_sub_official_info(self, official_info_model):
        try:
            Logger.logger.info('Update goods_sub Official Info Start')
            Logger.logger.info("db connect...")
            db = MysqlDatabase()
            Logger.logger.info("connect Success!!")

            goods_sub = db.selectQuery(self.query_select_goods_sub_item_no, official_info_model.item_no)

            if len(goods_sub) < 0:
                Logger.logger.info("not goods_sub info")
                Logger.logger.info("goods_sub info Insert Task Start")
                db.executeQuery(self.query_insert_goods_sub_init, official_info_model.item_no)
                Logger.logger.info("goods_sub info Insert Task Success!!!")

            sub_list = official_info_model.sub_info_list
            Logger.logger.info("goods_sub official info update Start!!")
            Logger.logger.info(len(sub_list))
            db.executeQuery(
                self.query_update_sub_goods_ofiicial_info, sub_list[0].get('AddValue'),
                sub_list[4].get('AddValue'), sub_list[1].get('AddValue'), sub_list[2].get('AddValue'),
                sub_list[3].get('AddValue'), official_info_model.item_no
            )
            Logger.logger.info("goods_sub official info update Success!!!!")
        except BaseException as e:
            Logger.logger.info("goods_sub Official Info DataBase Error")
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)
        return Utils().makeResponse(StrRepository().error_none)

    def update_goods_coupon_info(self, coupon_info):
        Logger.logger.info('Update goods coupon info start!')

        coupon_info = coupon_info.add_item_coupon
        Logger.logger.info('db connect...')
        db = MysqlDatabase()
        goods = db.selectQuery(self.query_select_goods_item_no2, coupon_info.get('GmktItemNo'))
        goods_sub = db.selectQuery(self.query_select_goods_sub_item_no, coupon_info.get('GmktItemNo'))
        Logger.logger.info('db connect success')

        Logger.logger.info(coupon_info)
        Logger.logger.info('[2]update')
        if (len(goods) > 0):
            if len(goods_sub) < 0:
                Logger.logger.info("not goods_sub info")
                Logger.logger.info("goods_sub info Insert Task Start")
                db.executeQuery(self.query_insert_goods_sub_init, coupon_info.get('GmktItemNo'))
                Logger.logger.info("goods_sub info Insert Task Success!!!")
            today = datetime.datetime.now()
            Logger.logger.info(self.query_update_goods_coupon_info_v2 % (today, coupon_info.get('AutoTermDuration'),
                                                                         coupon_info.get('AutoUseTermDuration'),
                                                                         coupon_info.get('UseInformation'),
                                                                         coupon_info.get('HelpDeskTelNo'),
                                                                         coupon_info.get('ApplyPlace'),
                                                                         coupon_info.get('ApplyPlaceUrl'),
                                                                         coupon_info.get('ApplyPlaceTelephone'),
                                                                         coupon_info.get('ServiceName'),
                                                                         coupon_info.get('ValidTermType'),
                                                                         coupon_info.get('AutoTermStartDay'),
                                                                         coupon_info.get('FixedTermStartDate'),
                                                                         coupon_info.get('FixedTermEndDate'),
                                                                         coupon_info.get('UseTermType'),
                                                                         coupon_info.get('AutoUseTermStartDay'),
                                                                         coupon_info.get('FixedUseTermStartDate'),
                                                                         coupon_info.get('FixedUseTermEndDate'),
                                                                         coupon_info.get('FindGuide'),
                                                                         coupon_info.get('PublicationCorp'),
                                                                         coupon_info.get('PublicationCorpWebUrl'),
                                                                         coupon_info.get('IsCancel'),
                                                                         coupon_info.get('CouponImageUrl'),
                                                                         coupon_info.get('GmktItemNo')))

            db.executeQuery(
                self.query_update_goods_coupon_info_v2, today, coupon_info.get('AutoTermDuration'),
                coupon_info.get('AutoUseTermDuration'), coupon_info.get('UseInformation'),
                coupon_info.get('HelpDeskTelNo'), coupon_info.get('ApplyPlace'), coupon_info.get('ApplyPlaceUrl'),
                coupon_info.get('ApplyPlaceTelephone'), coupon_info.get('ServiceName'),
                coupon_info.get('ValidTermType'),
                coupon_info.get('AutoTermStartDay'), coupon_info.get('FixedTermStartDate'),
                coupon_info.get('FixedTermEndDate'), coupon_info.get('UseTermType'),
                coupon_info.get('AutoUseTermStartDay'),
                coupon_info.get('FixedUseTermStartDate'), coupon_info.get('FixedUseTermEndDate'),
                coupon_info.get('FindGuide'), coupon_info.get('PublicationCorp'),
                coupon_info.get('PublicationCorpWebUrl'),
                coupon_info.get('IsCancel'), coupon_info.get('CouponImageUrl'), coupon_info.get('GmktItemNo')
            )
        else:
            Logger.logger.info('Faild! not Db in Goods')
            return Utils().makeResponse(StrRepository().error_coupon_regist_db)

        Logger.logger.info('[2]Update Goods Coupon Info Update Success')
        return Utils().makeResponse(StrRepository().error_none)

    def update_goods_price_info(self, price_info):
        Logger.logger.info('[0]Update goods price info start')

        price_info = price_info.add_price
        Logger.logger.info('[1]db connect')
        db = MysqlDatabase()
        goods = db.selectQuery(self.query_select_goods_item_no2, price_info.get('GmktItemNo'))
        Logger.logger.info('db connect success')

        Logger.logger.info(price_info)
        Logger.logger.info('[2]update')

        if (len(goods) > 0):
            today = datetime.datetime.now()

            db.executeQuery(self.query_update_goods_price_info, today, price_info.get('DisplayDate'),
                            price_info.get('StockQty'), price_info.get('GmktItemNo'))
        else:
            return Utils().makeResponse(StrRepository().error_coupon_regist)

        Logger.logger.info('[2]Update Goods price Info Update Success')
        return Utils().makeResponse(StrRepository().error_none)

    def selectGoods(self, start_date, end_date, item_no=None):
        db = MysqlDatabase()

        end_tmp = datetime.datetime.strptime(end_date, '%Y%m%d')
        end_tmp = end_tmp + datetime.timedelta(days=1)
        end_date = end_tmp.strftime('%Y%m%d')

        if (item_no != None and item_no != ''):
            goods = db.selectQuery(self.query_select_goods_item_no, start_date, end_date, item_no)
            return Utils().makeResponse(StrRepository().error_none, goods)
        else:
            goods_list = db.selectQuery(self.query_select_goods, start_date, end_date)
            return Utils().makeResponse(StrRepository().error_none, goods_list)
