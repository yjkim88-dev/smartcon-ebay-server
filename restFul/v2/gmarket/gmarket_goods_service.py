import html
import requests

from Logger import Logger
from .goods_regist_dao import GoodsRegistDao
from .gmarket_api_models import AddItem, gmarket_response


class GmarketGoodsService:
    api_url_add_item = 'http://tpl.gmarket.co.kr/v1/ItemService.asmx'
    headers = {'Content-Type': 'text/xml; charset=utf-8'}

    @classmethod
    def AddItem(cls, params):
        code = "00"
        result = "성공적으로 등록되었습니다."
        try:
            add_item_model = AddItem(params)
            user_id = params.get('user_id')
            add_item_code, add_item_result = add_item_model.set_xml()
            Logger.logger.info("===== AddItem API STEP1 set XML ====")
            Logger.logger.info(add_item_result)
            if add_item_code != "00":
                return -1, add_item_result

            Logger.logger.info("===== AddItem API STEP2 REQUEST ====")
            response = requests.post(
                url=cls.api_url_add_item,
                headers=cls.headers,
                data=add_item_result
            )
            Logger.logger.info("REQUEST SUCCESS")

            Logger.logger.info("===== AddItem API STEP3 RESPONSE PARSING ====")
            print(response.content.decode())
            Logger.logger.info(response.content.decode())

            add_item_res_code, add_item_res_msg = gmarket_response(response.content)

            if add_item_res_code != "00":
                Logger.logger.info("====AddItem API SETEP3 FAILD ====")
                Logger.logger.info(html.escape(add_item_res_msg))
                return -1, add_item_res_msg

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
                pass

        except BaseException as e:
            Logger.logger.info(e)
            return -1, "통신에러가 발생했습니다."
        return code, result

    @classmethod
    def postExcelGoods(cls, params):
        try:
            code, result = cls.AddItem(params)
            if code != "00":
                return code, result
            pass
        except BaseException as e:
            Logger.logger.info(e)
            return "-1", "통신에러가 발생했습니다."

        return code, result


