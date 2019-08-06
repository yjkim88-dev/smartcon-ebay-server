import html
import requests

from Logger import Logger
from .gmarket_api_models import AddItem


class GmarketGoodsService:
    api_url_add_item = 'http://tpl.gmarket.co.kr/v1/ItemService.asmx'
    headers = {'Content-Type': 'text/xml; charset=utf-8'}

    @classmethod
    def postGoodsBundle(cls, params):
        add_item_code, add_item_result = AddItem(params).set_xml()
        if add_item_code != "00":
            return -1, add_item_result

        response = requests.post(
            url= cls.api_url_add_item,
            hedaer=cls.headers,
            data = add_item_result
        )

        print(response.content)
        Logger.logger.info(response.content)



