import html
import requests

from Logger import Logger
from .goods_regist_dao import GoodsRegistDao
from .gmarket_api_models import AddItem, OfficialInfo, gmarket_response
from restFul.repository import StrRepository
from restFul.utils import Utils


class GmarketGoodsService:
    api_url_add_item = 'http://tpl.gmarket.co.kr/v1/ItemService.asmx'
    headers = {'Content-Type': 'text/xml; charset=utf-8'}

    @classmethod
    def postExcelGoods(cls, params):
        try:
            params['item_no'] = cls.add_gmarket_item(params)
            cls.add_gmarket_official_info(params)
        except BaseException as e:
            Logger.logger.info(e)
            return Utils().makeResponse(("-1", "통신오류가 발생했습니다."))

    @classmethod
    def add_gmarket_item(cls, params):
        try:
            add_item_model = AddItem(params)
            user_id = params.get('user_id')
            add_item_xml = add_item_model.set_xml()

            Logger.logger.info("===== AddItem API STEP2 REQUEST ====")
            response = requests.post(
                url=cls.api_url_add_item,
                headers=cls.headers,
                data=add_item_xml
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

        return item_no

    @classmethod
    def add_gmarket_official_info(cls, params):
        Logger.logger.info("==== AddOfficialInfo API Start")
        try:
            official_info_model = OfficialInfo(params)
            official_info_xml = official_info_model.set_xml()

            Logger.logger.info("===== OfficialInfo API STEP2 REQUEST ====")
            response = requests.post(
                url=cls.api_url_add_item,
                headers=cls.headers,
                data=official_info_xml
            )

            Logger.logger.info("REQUEST SUCCESS")

            Logger.logger.info("===== OfficialInfo API STEP3 RESPONSE PARSING ====")
            print(response.content.decode())
            Logger.logger.info(response.content.decode())

            add_official_res_code, add_official_res_msg = gmarket_response('AddOfficialInfo',response.content)

            if add_official_res_code != "00":
                Logger.logger.info("====OfficialInfo API SETEP3 FAILD ====")

                Logger.logger.info(html.escape(add_official_res_msg))
                return Utils().makeResponse(StrRepository().error_official_regist)

            Logger.logger.info("==== PARSING SUCCESS ====")
            Logger.logger.info(add_official_res_msg)

        except BaseException as e:
            Logger.logger.info("====OfficialInfo API FAILD ====")
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_goods_regist)

        Logger.logger.info("====OfficialInfo API Success ====")
