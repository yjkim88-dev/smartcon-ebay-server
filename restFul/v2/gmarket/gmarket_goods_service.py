import html
import requests

from Logger import Logger
from .gmarket_api_models import AddItem, gmarket_response


class GmarketGoodsService:
    api_url_add_item = 'http://tpl.gmarket.co.kr/v1/ItemService.asmx'
    headers = {'Content-Type': 'text/xml; charset=utf-8'}

    @classmethod
    def postGoodsBundle(cls, params):
        try:
            add_item_code, add_item_result = AddItem(params).set_xml()
            if add_item_code != "00":
                return -1, add_item_result

            response = requests.post(
                url= cls.api_url_add_item,
                headers=cls.headers,
                data = add_item_result
            )

            Logger.logger.info("===== STEP1 RESPONSE ====")
            print(response.content)
            Logger.logger.info(response.content)

            add_item_res_code, add_item_res_msg = gmarket_response(response.content)

            if add_item_res_code != "00":
                Logger.logger.info("==== SETEP1 FAILD ====")
                Logger.logger.info(html.escape(add_item_res_msg))
                return -1, add_item_res_msg


        except Exception as e:
            Logger.logger.info("error:"+ e)
            return -1, "통신에러가 발생했습니다."


