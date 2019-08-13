import html
import requests

from Logger import Logger
from .goods_regist_dao import GoodsRegistDao
from .gmarket_api_models import AddItem, OfficialInfo, CouponInfo, PriceInfo, gmarket_response
from restFul.repository import StrRepository
from restFul.utils import Utils


class GmarketGoodsService:
    api_url_add_item = 'http://tpl.gmarket.co.kr/v1/ItemService.asmx'
    headers = {'Content-Type': 'text/xml; charset=utf-8'}

    @classmethod
    def postExcelGoods(cls, params):
        try:
            result = cls.add_gmarket_item(params)
            if result.get('errorCode') != "00":
                return result

            params['item_no'] = result.get('results')
            result = cls.add_gmarket_official_info(params)
            if result.get('errorCode') != "00":
                return result

            result = cls.add_gmarket_coupon_info(params)
            if result.get('errorCode') != "00":
                return result

            result = cls.add_gmarket_price_info(params)
            if result.get('errorCode') != "00":
                return result

        except BaseException as e:
            Logger.logger.info(e)
            return Utils().makeResponse(("-1", "통신오류가 발생했습니다."))
        return Utils().makeResponse(StrRepository().error_none)

    @classmethod
    def add_gmarket_item(cls, params):
        try:
            add_item_model = AddItem(params)
            user_id = params.get('user_id')
            xml_result = add_item_model.set_xml()

            if xml_result.get('errorCode') != '00':
                return Utils().makeResponse(StrRepository().error_goods_regist)

            Logger.logger.info("===== AddItem API STEP2 REQUEST ====")

            response = requests.post(
                url=cls.api_url_add_item,
                headers=cls.headers,
                data=xml_result.get('results')
            )
            Logger.logger.info("REQUEST SUCCESS")

            Logger.logger.info("===== AddItem API STEP3 RESPONSE PARSING ====")
            print(response.content.decode())
            Logger.logger.info(response.content.decode())

            add_item_res_code, add_item_res_msg = gmarket_response('AddItem', response.content)

            if add_item_res_code != "00":
                Logger.logger.info("====AddItem API SETEP3 FAILD ====")
                Logger.logger.info(html.escape(add_item_res_msg))
                return Utils().makeResponse(StrRepository().error_goods_regist)

            Logger.logger.info("==== PARSING SUCCESS ====")
            Logger.logger.info(add_item_res_msg)

            try:
                Logger.logger.info("==== AddItem API STEP4 Insert DB ====")
                item_no = add_item_res_msg['GmktItemNo']

                add_item_model.shipping['GroupCode'] = \
                    add_item_res_msg.get('ShippingGroupCode') \
                        if add_item_res_msg.get('ShippingGroupCode') is not None \
                        else add_item_model.shipping.get('GroupCode')

                GoodsRegistDao().insertGoods(item_no, add_item_model, user_id)

            except BaseException as e:
                Logger.logger.info("==== AddItem API STEP4 Failed Insert DB ====")
                Logger.logger.info(e)
                return Utils().makeResponse(StrRepository().error_goods_regist)

        except BaseException as e:
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_goods_regist)

        Logger.logger.info("==== AddItem API Success ====")

        return Utils().makeResponse(StrRepository().error_none, item_no)

    @classmethod
    def add_gmarket_official_info(cls, params):
        Logger.logger.info("==== AddOfficialInfo API Start")
        try:
            official_info_model = OfficialInfo(params)
            official_xml_result = official_info_model.set_xml()

            if official_xml_result.get('errorCode') != "00":
                return official_xml_result

            Logger.logger.info("===== AddOfficialInfo API STEP2 REQUEST ====")
            response = requests.post(
                url=cls.api_url_add_item,
                headers=cls.headers,
                data=official_xml_result.get('results')
            )

            Logger.logger.info("REQUEST SUCCESS")

            Logger.logger.info("===== AddOfficialInfo API STEP3 RESPONSE PARSING ====")
            print(response.content.decode())
            Logger.logger.info(response.content.decode())

            add_official_res_code, add_official_res_msg = gmarket_response('AddOfficialInfo',response.content)

            if add_official_res_code != "00":
                Logger.logger.info("====AddOfficialInfo API SETEP3 FAILD ====")

                Logger.logger.info(html.escape(add_official_res_msg))
                return Utils().makeResponse(StrRepository().error_official_regist)

            if add_official_res_msg.get('Result') == 'Fail':
                Logger.logger.info("====AddOfficialInfo API SETEP3 FAILD ====")
                Logger.logger.info(html.escape(add_official_res_msg))
                return Utils().makeResponse(StrRepository().error_official_regist)

            Logger.logger.info("==== PARSING SUCCESS ====")
            Logger.logger.info(add_official_res_msg)

        except BaseException as e:
            Logger.logger.info("====OfficialInfo API FAILD ====")
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_official_regist)

        Logger.logger.info("====OfficialInfo API Success ====")
        return Utils().makeResponse(StrRepository().error_none)

    @classmethod
    def add_gmarket_coupon_info(cls, params):
        Logger.logger.info("==== AddCouponInfo API Start")
        try:
            coupon_info_model = CouponInfo(params)
            coupon_xml_result = coupon_info_model.set_xml()

            if coupon_xml_result.get('errorCode') != "00":
                return coupon_xml_result

            Logger.logger.info("===== AddCouponInfo API STEP2 REQUEST Task====")

            response = requests.post(
                url=cls.api_url_add_item,
                headers=cls.headers,
                data=coupon_xml_result.get('results')
            )

            Logger.logger.info("REQUEST Task SUCCESS ")

            Logger.logger.info("===== AddCouponInfo API STEP3 RESPONSE PARSING ====")
            print(response.content.decode())
            Logger.logger.info(response.content.decode())

            add_coupon_res_code, add_coupon_res_msg = gmarket_response('AddItemCoupon', response.content)

            if add_coupon_res_code != "00":
                Logger.logger.info("====AddCouponInfo API SETEP3 FAILD ====")

                Logger.logger.info(html.escape(add_coupon_res_msg))
                return Utils().makeResponse(StrRepository().error_coupon_regist)

            if add_coupon_res_msg.get('Result') == 'Fail':
                Logger.logger.info("====AddCouponInfo API SETEP3 FAILD ====")
                Logger.logger.info(html.escape(add_coupon_res_msg.get('Comment')))
                return Utils().makeResponse(StrRepository().error_coupon_regist)

            Logger.logger.info("==== AddCouponInfo SUCCESS ====")
            Logger.logger.info(add_coupon_res_msg)

            try:
                Logger.logger.info("==== AddCouponInfo API STEP4 Insert DB ====")
                GoodsRegistDao().update_goods_coupon_info(coupon_info_model)

            except BaseException as e:
                Logger.logger.info("==== AddCouponInfo API STEP4 Failed Insert DB ====")
                Logger.logger.info(e)
                return Utils().makeResponse(StrRepository().error_coupon_regist)

        except BaseException as e:
            Logger.logger.info("====AddCouponInfo API FAILD ====")
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_coupon_regist)

        return Utils().makeResponse(StrRepository().error_none)

    @classmethod
    def add_gmarket_price_info(cls, params):
        Logger.logger.info("==== AddPriceInfo API Start")
        try:
            price_info_model = PriceInfo(params)
            price_xml_result = price_info_model.set_xml()

            if price_xml_result.get('errorCode') != "00":
                return price_xml_result

            Logger.logger.info("===== AddPriceInfo API STEP2 REQUEST Task====")

            response = requests.post(
                url=cls.api_url_add_item,
                headers=cls.headers,
                data=price_xml_result.get('results')
            )

            Logger.logger.info("REQUEST Task SUCCESS ")

            Logger.logger.info("===== AddPriceInfo API STEP3 RESPONSE PARSING ====")
            print(response.content.decode())
            Logger.logger.info(response.content.decode())

            add_coupon_res_code, add_coupon_res_msg = gmarket_response('AddPrice', response.content)

            if add_coupon_res_code != "00":
                Logger.logger.info("====AddPriceInfo API SETEP3 FAILD ====")

                Logger.logger.info(html.escape(add_coupon_res_msg))
                return Utils().makeResponse(StrRepository().error_price_regist)

            if add_coupon_res_msg.get('Result') == 'Fail':
                Logger.logger.info("====AddPriceInfo API SETEP3 FAILD ====")
                Logger.logger.info(html.escape(add_coupon_res_msg.get('Comment')))
                return Utils().makeResponse(StrRepository().error_price_regist)

            Logger.logger.info("==== AddPriceInfo SUCCESS ====")
            Logger.logger.info(add_coupon_res_msg)

            try:
                Logger.logger.info("==== AddPriceInfo API STEP4 Insert DB ====")
                GoodsRegistDao().update_goods_price_info(price_info_model)

            except BaseException as e:
                Logger.logger.info("==== AddPriceInfo API STEP4 Failed Insert DB ====")
                Logger.logger.info(e)
                return Utils().makeResponse(StrRepository().error_price_regist)

        except BaseException as e:
            Logger.logger.info("====AddPriceInfo API FAILD ====")
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_price_regist)

        return Utils().makeResponse(StrRepository().error_none)