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

            # response = requests.post(
            #     url= cls.api_url_add_item,
            #     headers=cls.headers,
            #     data = add_item_result
            # )
            response = {
                "content" :  b'<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><soap:Fault><faultcode>soap:Client</faultcode><faultstring>\xec\x84\x9c\xeb\xb2\x84\xec\x97\x90\xec\x84\x9c \xec\x9a\x94\xec\xb2\xad\xec\x9d\x84 \xec\x9d\xbd\xec\x9d\x84 \xec\x88\x98 \xec\x97\x86\xec\x8a\xb5\xeb\x8b\x88\xeb\x8b\xa4. ---&gt; XML \xeb\xac\xb8\xec\x84\x9c(10, 1057)\xec\x97\x90 \xec\x98\xa4\xeb\xa5\x98\xea\xb0\x80 \xec\x9e\x88\xec\x8a\xb5\xeb\x8b\x88\xeb\x8b\xa4. ---&gt; \xec\x9d\xb8\xec\x8a\xa4\xed\x84\xb4\xec\x8a\xa4 \xec\x9c\xa0\xed\x9a\xa8\xec\x84\xb1 \xea\xb2\x80\xec\x82\xac \xec\x98\xa4\xeb\xa5\x98: \'free\'\xec\x9d\x80(\xeb\x8a\x94) TaxEnum\xec\x97\x90 \xec\x82\xac\xec\x9a\xa9\xed\x95\xa0 \xec\x88\x98 \xec\x97\x86\xeb\x8a\x94 \xea\xb0\x92\xec\x9e\x85\xeb\x8b\x88\xeb\x8b\xa4.</faultstring><detail /></soap:Fault></soap:Body></soap:Envelope>\r\n'
            }
            Logger.logger.info("===== STEP1 RESPONSE ====")
            print(response.get('content').decode())
            Logger.logger.info(response.get('content').decode())

            add_item_res_code, add_item_res_msg = gmarket_response(response.get('content'))

            if add_item_res_code != "00":
                Logger.logger.info("==== SETEP1 FAILD ====")
                Logger.logger.info(html.escape(add_item_res_msg))
                return -1, add_item_res_msg

            Logger.logger.info("==== SETEP1 SUCCESS ====")
            Logger.logger.info(html.escape(add_item_res_msg))

        except Exception as e:
            Logger.logger.info("error:"+ e)
            return -1, "통신에러가 발생했습니다."


