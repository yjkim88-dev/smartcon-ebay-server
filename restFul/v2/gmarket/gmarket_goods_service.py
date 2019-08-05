import html

from .gmarket_api_models import AddItem


class GmarketGoodsService:
    @classmethod
    def postGoodsBundle(cls, params):
        cls.postAddItem(params)
        pass

    @classmethod
    def postAddItem(cls,params):
        add_item_xml = AddItem(params).set_xml()
        print(add_item_xml)

