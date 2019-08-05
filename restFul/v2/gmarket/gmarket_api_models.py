import xml.etree.ElementTree as ET
import html

from restFul.config import encticket


class AddItem:
    namespace = {
        'soap': "http://schemas.xmlsoap.org/soap/envelope/",
        'base': "http://tpl.gmarket.co.kr/",
        'xsd': "http://tpl.gmarket.co.kr/tpl.xsd"
    }

    def __init__(self, params={}):
        self.add_item = {
            "out_item_no": params.get('out_item_no'),
            "category_code": params.get('category_code'),
            "gmkt_item_no": params.get('gmkt_item_no'),
            "item_name": params.get('item_name'),
            "item_eng_name": params.get('item_eng_name'),
            "item_description": params.get('item_description'),
            "gd_html": html.escape(params.get('gd_html')).replace('"', '&quot;') \
                if params.get('gd_html') is not None else None,
            "gd_add_html": params.get('gd_add_html'),
            "gd_prmt_html": params.get('gd_prmt_html'),
            "maker_no": params.get('maker_no'),
            "brand_no": params.get('brand_no'),
            "model_name": params.get('model_name'),
            "is_adult": params.get('is_adult', "false"),
            "tax": params.get('tax', "free"),
            "free_gift": params.get('free_gift'),
            "item_kind": params.get('item_kind', "Ecoupon")
        }

        self.reference_price = {
            "kind": params.get("kind", "Quotation"),
            "price": params.get("price")
        }

        self.ref_usal = {
            "is_price_compare": params.get('is_price_compare', "false"),
            "is_nego": params.get('is_nego', "false"),
            "is_jaehu_discount": params.get('is_jaehu_discount', "false")
        }

        self.item_image = {
            "default_image": params.get('default_image'),
            "large_image": params.get('large_image'),
            "small_image": params.get('small_image')
        }

        self.item_as = {
            "telephone": params.get("telephone", "02-561-0671"),
            "address": params.get("address", "Seller")
        }

        self.shipping = {
            "set_type": params.get('set_type', "Use"),
            "group_code": params.get('group_code', 136),
            "refund_addr_num": params.get('refund_addr_num', "0"),
            "trans_policy_no": params.get('trans_policy_no', "38174"),
            "new_item_shipping": {
                "fee_condition": params.get('fee_condition', "Free"),
                "fee_base_price": params.get('fee_base_price', "0"),
                "fee": params.get('fee', "0")
            }
        }

        self.bundle_order = {
            "buy_unit_count": params.get('buy_unit_count', "1"),
            "min_buy_count": params.get('min_buy_count', "1"),
        }

        self.order_limit = {
            "order_limit_count": params.get('order_limit_count', "0"),
            "order_limit_period": params.get('order_limit_period', "0")
        }

        self.origin = {
            "code": params.get('code', "Domestic"),
            "place": params.get('place', "서울시 역삼동")
        }

        self.goods_kind = {
            "goods_kind": params.get('goods_kind', "New"),
            "goods_status": params.get('goods_status', "Fine"),
            "goods_tag": params.get('goods_tag', "New")
        }

    def set_xml(self):
        tree = ET.parse("../xmls/add_item.xml")
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

        add_item.attrib['OutItemNo']        = self.add_item.get('out_item_no')
        add_item.attrib['CategoryCode']     = self.add_item.get('category_code')
        add_item.attrib['GmktItemNo']       = self.add_item.get('gmkt_item_no')
        add_item.attrib['ItemName']         = self.add_item.get('item_name')
        add_item.attrib['ItemEngName']      = self.add_item.get('item_eng_name')
        add_item.attrib['ItemDescription']  = self.add_item.get('item_description')
        add_item.attrib['GdHtml']           = self.add_item.get('gd_html')
        add_item.attrib['GdAddHtml']        = self.add_item.get('gd_add_html')
        add_item.attrib['GdPrmtHtml']       = self.add_item.get('gd_prmt_html')
        add_item.attrib['MakerNo']          = self.add_item.get('maker_no')
        add_item.attrib['BrandNo']          = self.add_item.get('brand_no')
        add_item.attrib['ModelName']        = self.add_item.get('model_name')
        add_item.attrib['IsAdult']          = self.add_item.get('is_adult')
        add_item.attrib['Tax']              = self.add_item.get('tax')
        add_item.attrib['FreeGift']         = self.add_item.get('free_gift')
        add_item.attrib['ItemKind']         = self.add_item.get('item_kind')

        reference_price.attrib['Kind']      = self.reference_price.get('kind')
        reference_price.attrib['Price']     = self.reference_price.get('price')

        ref_usal.attrib['IsPriceCompare']   = self.ref_usal.get('is_price_compare')
        ref_usal.attrib['IsNego']           = self.ref_usal.get('is_nego')
        ref_usal.attrib['IsJaehuDiscount']  = self.ref_usal.get('is_jaehu_discount')

        item_image.attrib['DefaultImage']   = self.item_image.get('default_image')
        item_image.attrib['LargeImage']     = self.item_image.get('large_image')
        item_image.attrib['SmallImage']     = self.item_image.get('small_image')

        item_as.attrib['Telephone']         = self.item_as.get('telephone')
        item_as.attrib['Address']           = self.item_as.get('address')

        shipping.attrib['SetType']          = self.shipping.get('set_type')
        shipping.attrib['GroupCode']        = self.shipping.get('group_code')
        shipping.attrib['RefundAddrNum']    = self.shipping.get('refund_addr_num')
        shipping.attrib['TransPolicyNo']    = self.shipping.get('trans_policy_no')
        new_item_shipping['FeeCondition']   = self.shipping.get('new_item_shipping').get('fee_condition')
        new_item_shipping['FeeBasePrice']   = self.shipping.get('new_item_shipping').get('fee_base_price')
        new_item_shipping['Fee']            = self.shipping.get('new_item_shipping').get('fee')

        bundle_order.attrib['BuyUnitCount'] = self.bundle_order.get('buy_unit_count')
        bundle_order.attrib['MinBuyCount']  = self.bundle_order.get('min_buy_count')

        order_limit.attrib['OrderLimitCount']   = self.order_limit.get('order_limit_count')
        order_limit.attrib['OrderLimitPeriod']  = self.order_limit.get('order_limit_period')

        origin.attrib['Code']               = self.origin.get('code')
        origin.attrib['Place']              = self.origin.get('place')

        goods_kind.attrib['GoodsKind']      = self.goods_kind.get('goods_kind')
        goods_kind.attrib['GoodsStatus']    = self.goods_kind.get('goods_status')
        goods_kind.attrib['GoodsTag']       = self.goods_kind.get('goods_tag')

        return ET.tostring(root ,encoding='utf8', method='xml')




