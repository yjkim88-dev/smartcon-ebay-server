import xml.etree.ElementTree as ET
import os
import html

from Logger import Logger
from restFul.config import encticket
from restFul.utils import Utils

xml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'xmls')

class AddItem:
    namespace = {
        'soap': "http://schemas.xmlsoap.org/soap/envelope/",
        'base': "http://tpl.gmarket.co.kr/",
        'xsd': "http://tpl.gmarket.co.kr/tpl.xsd"
    }

    def __init__(self, params={}):
        self.add_item = {
            "OutItemNo": params.get('out_item_no'),
            "CategoryCode": params.get('category_code'),
            "GmktItemNo": params.get('gmkt_item_no'),
            "ItemName": params.get('item_name'),
            "ItemEngName": params.get('item_eng_name'),
            "ItemDescription": params.get('item_description'),
            "GdHtml": html.escape(params.get('gd_html')).replace('"', '&quot;') \
                if params.get('gd_html') is not None else None,
            "GdAddHtml": params.get('gd_add_html'),
            "GdPrmtHtml": params.get('gd_prmt_html'),
            "MakerNo": params.get('maker_no'),
            "BrandNo": params.get('brand_no'),
            "ModelName": params.get('model_name'),
            "IsAdult": params.get('is_adult', "false"),
            "Tax": params.get('tax', "free"),
            "FreeGift": params.get('free_gift'),
            "ItemKind": params.get('item_kind', "Ecoupon")
        }

        self.reference_price = {
            "Kind": params.get("kind", "Quotation"),
            "Price": params.get("price")
        }

        self.ref_usal = {
            "IsPriceCompare": params.get('is_price_compare', "false"),
            "IsNego": params.get('is_nego', "false"),
            "IsJaehuDiscount": params.get('is_jaehu_discount', "false")
        }

        self.item_image = {
            "DefaultImage": params.get('default_image'),
            "LargeImage": params.get('large_image'),
            "SmallImage": params.get('small_image')
        }

        self.item_as = {
            "Telephone": params.get("telephone", "02-561-0671"),
            "Address": params.get("address", "Seller")
        }

        self.shipping = {
            "SetType": params.get('set_type', "Use"),
            "GroupCode": params.get('group_code', 136),
            "RefundAddrNum": params.get('refund_addr_num', "0"),
            "TransPolicyNo": params.get('trans_policy_no', "38174"),
            "new_item_shipping": {
                "FeeCondition": params.get('fee_condition', "Free"),
                "FeeBasePrice": params.get('fee_base_price', "0"),
                "Fee": params.get('fee', "0")
            }
        }

        self.bundle_order = {
            "BuyUnitCount": params.get('buy_unit_count', "1"),
            "MinBuyCount": params.get('min_buy_count', "1"),
        }

        self.order_limit = {
            "OrderLimitCount": params.get('order_limit_count', "0"),
            "OrderLimitPeriod": params.get('order_limit_period', "0")
        }

        self.origin = {
            "Code": params.get('code', "Domestic"),
            "Place": params.get('place', "서울시 역삼동")
        }

        self.goods_kind = {
            "GoodsKind": params.get('goods_kind', "New"),
            "GoodsStatus": params.get('goods_status', "Fine"),
            "GoodsTag": params.get('goods_tag', "New")
        }

    def set_xml(self):
        try:
            tree = ET.parse(os.path.join(xml_path, "add_item.xml"))
            root = tree.getroot()

            encTicket = root.find("soap:Header", self.namespace). \
                find('base:EncTicket', self.namespace). \
                find('base:encTicket', self.namespace)

            encTicket.text = encticket

            add_item = root.find("soap:Body", self.namespace) \
                .find('base:AddItem', self.namespace) \
                .find("base:AddItem", self.namespace)

            reference_price = add_item.find('xsd:ReferencePrice', self.namespace)
            ref_usal = add_item.find('xsd:Refusal', self.namespace)
            item_image = add_item.find('xsd:ItemImage', self.namespace)
            item_as = add_item.find('xsd:As', self.namespace)
            shipping = add_item.find('xsd:Shipping', self.namespace)
            new_item_shipping = shipping.find('xsd:NewItemShipping',self.namespace)
            bundle_order = add_item.find('xsd:BundleOrder', self.namespace)
            order_limit = add_item.find('xsd:OrderLimit', self.namespace)
            origin = add_item.find('xsd:Origin', self.namespace)
            goods_kind = add_item.find('xsd:GoodsKind', self.namespace)


            for key, value in self.add_item.items():
                Utils.set_xml_element_attrib(add_item, key, value)

            for key, value in self.reference_price.items():
                Utils.set_xml_element_attrib(reference_price, key, value)

            for key, value in self.ref_usal.items():
                Utils.set_xml_element_attrib(ref_usal, key, value)

            for key, value in self.item_image.items():
                Utils.set_xml_element_attrib(item_image, key, value)

            for key, value in self.item_as.items():
                Utils.set_xml_element_attrib(item_as, key, value)

            for key, value in self.shipping.items():
                if key == 'new_item_shipping':
                    for new_key, new_value in value.items():
                        Utils.set_xml_element_attrib(new_item_shipping, new_key, new_value)
                else:
                    Utils.set_xml_element_attrib(shipping, key, value)

            for key, value in self.bundle_order.items():
                Utils.set_xml_element_attrib(bundle_order, key, value)

            for key, value in self.order_limit.items():
                Utils.set_xml_element_attrib(order_limit, key, value)

            for key, value in self.origin.items():
                Utils.set_xml_element_attrib(origin, key, value)

            for key, value in self.goods_kind.items():
                Utils.set_xml_element_attrib(goods_kind, key, value)

            result = ET.tostring(root ,encoding='utf8', method='xml')
            code = "00"
        except Exception as e:
            Logger.logger.info(e)
            code = "-1"
            result = e

        Logger.logger.info("====== STEP1 AddItem =====")
        Logger.logger.info(result)
        return code, result




