import xml.etree.ElementTree as ET
import os
import requests

from Logger import Logger
from restFul.config import encticket
from restFul.utils import Utils
from restFul.repository import StrRepository
xml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'xmls')

## API 파라미터 명과 클래스 파라미터 명이 다른 경우 동일한 사용자 입력값을 활용하는 경우다.

class AddItem:
    namespace = {
        'soap': "http://schemas.xmlsoap.org/soap/envelope/",
        'base': "http://tpl.gmarket.co.kr/",
        'xsd': "http://tpl.gmarket.co.kr/tpl.xsd"
    }

    # 지마켓 SOAP XML API 요청후 응답 XML의 요소명의 prefix를 name으로 사용
    # ex <AddItemResponse> => name = AddItem
    name = "AddItem"

    def __init__(self, params={}):
        expiration_date = str(params.get('expiration_date'))
        expiration_date = Utils().convertStringDateToM(expiration_date)

        self.user_id = params.get('user_id')

        self.add_item = {
            "OutItemNo": params.get('out_item_no'),
            "CategoryCode": params.get('category_code'),
            "GmktItemNo": params.get('item_no'),
            "ItemName": params.get('item_name'),
            "ItemEngName": params.get('item_eng_name'),
            "ItemDescription": params.get('item_description'),
            "GdHtml": params.get('gd_html'),
            "GdAddHtml": params.get('gd_add_html', ''),
            "GdPrmtHtml": params.get('gd_prmt_html', ''),
            "MakerNo": params.get('maker_no'),
            "BrandNo": params.get('brand_no'),
            "ModelName": params.get('model_name'),
            "IsAdult": params.get('is_adult', "false"),
            "Tax": params.get('tax', "Free"),
            "FreeGift": params.get('free_gift'),
            "ItemKind": params.get('item_kind', "Ecoupon"),
            "ExpirationDate": expiration_date
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


        except Exception as e:
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_goods_regist)
        result = ET.tostring(root, encoding='utf8', method='xml')

        Logger.logger.info("==== AddItem API xml success ====")
        Logger.logger.info(result.decode())
        return Utils().makeResponse(StrRepository().error_none, result)


class OfficialInfo:
    namespace = {
        'soap': "http://schemas.xmlsoap.org/soap/envelope/",
        'base': "http://tpl.gmarket.co.kr/",
        'xsd': "http://tpl.gmarket.co.kr/tpl.xsd"
    }

    name = "AddOfficialInfo"

    def __init__(self, params):
        self.item_no = str(params.get('item_no', ''))
        self.group_code = params.get('GroupCode', '37')
        self.sub_info_list = [
            {"Code": '37-1', "AddYn": 'Y', "AddValue": params.get('issuer',"(주)스마트콘") },
            {"Code": '37-2', "AddYn": 'Y', "AddValue": params.get('official_expiration_date_or_use_condition',"상품별상이 / 상세페이지참고 (프로모션 상품 예외)") },
            {"Code": '37-3', "AddYn": 'Y', "AddValue": params.get('use_brand', "상품 상세 페이지에 제공")},
            {"Code": '37-4', "AddYn": 'Y', "AddValue": params.get('refund_condition_and_rule', "상품 상세 페이지에 제공") },
            {"Code": '37-5', "AddYn": 'Y', "AddValue": params.get('counsel_tel_no', "02-561-0671")}
        ]

        # self.trade_info_list = [
        #     {"Code": '999-1', "AddYn": 'N', "AddValue": "상품 상세 페이지에 제공"},
        #     {"Code": '999-2', "AddYn": 'N', "AddValue": "상품 상세 페이지에 제공"},
        #     {"Code": '999-3', "AddYn": 'N', "AddValue": "상품 상세 페이지에 제공"},
        #     {"Code": '999-4', "AddYn": 'N', "AddValue": "상품 상세 페이지에 제공"},
        #     {"Code": '999-5', "AddYn": 'N', "AddValue": "상품 상세 페이지에 제공"}
        # ]

    def set_xml(self):
        try:
            Logger.logger.info("==== OfficialInfo API xml create ====")
            Logger.logger.info("==== OfficialInfo API xml parsing ====")
            Logger.logger.info("==== OfficialInfo API xml parsing success====")
            tree = ET.parse(os.path.join(xml_path, "official_info.xml"))
            root = tree.getroot()

            encTicket = root.find("soap:Header", self.namespace). \
                find('base:EncTicket', self.namespace). \
                find('base:encTicket', self.namespace)

            Logger.logger.info("==== OfficialInfo API xml encTicket Setting Success ====")


            encTicket.text = encticket

            AddOfficialInfo = root.find('soap:Body', self.namespace). \
                find('base:AddOfficialInfo', self.namespace). \
                find('base:AddOfficialInfo', self.namespace)

            AddOfficialInfo.attrib['GmktItemNo'] = self.item_no
            AddOfficialInfo.attrib['GroupCode'] = self.group_code

            sub_info_list = AddOfficialInfo.findall('xsd:SubInfoList', self.namespace)

            # 쿠폰쪽에서는 안써도 무관한 거래정보 혹시 나중에 필요하시면 사용.
            # trade_info_list = AddOfficialInfo.findall('xsd:TradeInfoList', self.namespace)

            if len(sub_info_list) > len(self.sub_info_list):
                Logger.logger.info('필요한 sub_info_list 요소보다 파라미터 sub_info_list 값이 적습니다.')
                return Utils().makeResponse(StrRepository().error_official_regist)
            

            # if len(trade_info_list) > len(self.trade_info_list):
            #     Logger.logger.info('필요한 trade_info_list 요소보다 파라미터 trade_info_list 값이 적습니다.')
            #     return Utils().makeResponse(StrRepository().error_official_regist)

            for idx in range(len(sub_info_list)):
                sub_info_list[idx].attrib['Code'] = self.sub_info_list[idx].get('Code','')
                sub_info_list[idx].attrib['AddYn'] = self.sub_info_list[idx].get('AddYn','')
                sub_info_list[idx].attrib['AddValue'] = self.sub_info_list[idx].get('AddValue','')

            # for idx in range(len(trade_info_list)):
            #     trade_info_list[idx].attrib['Code'] = self.trade_info_list[idx].get('Code', '')
            #     trade_info_list[idx].attrib['AddYn'] = self.trade_info_list[idx].get('AddYn', '')
            #     trade_info_list[idx].attrib['AddValue'] = self.trade_info_list[idx].get('AddValue', '')

            Logger.logger.info("==== OfficialInfo API xml body setting Success ====")
        except BaseException as e:
            Logger.logger.info('Official Info create xml Failed')
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_official_regist)

        result = ET.tostring(root, encoding='utf8', method='xml')

        Logger.logger.info("==== OfficialInfo API xml Success ====")
        Logger.logger.info(result.decode())

        return Utils().makeResponse(StrRepository().error_none, result)


class CouponInfo:
    namespace = {
        'soap': "http://schemas.xmlsoap.org/soap/envelope/",
        'base': "http://tpl.gmarket.co.kr/",
        'xsd': "http://tpl.gmarket.co.kr/tpl.xsd"
    }
    name = "AddItemCoupon"
    def __init__(self, params):
        fixed_term_start_date = Utils().convertStringDateToM(params.get('fixed_term_start_date')) if params.get('fixed_term_start_date') is not None else None
        fixed_term_end_date  = Utils().convertStringDateToM(params.get('fixed_term_end_date')) if params.get('fixed_term_end_date') is not None else None
        fixed_use_term_start_date = Utils().convertStringDateToM(params.get('fixed_use_term_start_date')) if params.get('fixed_use_term_start_date') is not None else None
        fixed_use_term_end_date = Utils().convertStringDateToM(params.get('fixed_use_term_end_date')) if params.get('fixed_use_term_end_date') is not None else None
        self.add_item_coupon = {
            'GmktItemNo' : str(params.get('item_no', '')),
            'CouponType' : params.get('coupon_type', 'Mobile'),
            'CouponMoneyType' : params.get('coupon_money_type', 'FixedAmount'),
            'CouponMoney' : params.get('coupon_money') if params.get('coupon_money') is not None else params.get('price'),
            'ServiceName' : params.get('service_name') if params.get('service_name') is not None else params.get('item_name'),
            'CouponImageUrl' : params.get('coupon_image_url') if params.get('coupon_image_url') is not None else params.get('default_image'),
            'ValidTermType' : params.get('valid_term_type', 'AutoTerm'),
            'AutoTermStartDay' : params.get('auto_term_start_day'),
            'AutoTermDuration' : params.get('auto_term_duration'),
            'FixedTermStartDate' : fixed_term_start_date,
            'FixedTermEndDate' : fixed_term_end_date,
            'UseTermType' : params.get('use_term_type', 'AutoTerm'),
            'AutoUseTermStartDay' : params.get('auto_use_term_start_day'),
            'AutoUseTermDuration' : params.get('auto_use_term_duration'),
            'FixedUseTermStartDate': fixed_use_term_start_date,
            'FixedUseTermEndDate' : fixed_use_term_end_date,
            'UseInformation' : params.get('use_information', ''),
            'HelpDeskTelNo' : params.get('help_desk_telno', ''),
            'ApplyPlace' : params.get('apply_place', ''),
            'ApplyPlaceUrl': params.get('apply_place_url', ''),
            'ApplyPlaceTelephone' : params.get('apply_place_telephone', ''),
            'AddBenefit' : params.get('add_bene_fit', ''),
            'RestrictCondition' : params.get('restrict_condition', ''),
            'FindGuide' : params.get('find_guide'),
            'PublicationCorp' : params.get('publication_corp'),
            'PublicationCorpWebUrl' : params.get('publication_corp_web_url', ''),
            'IsCustomerNameView' : params.get('is_customer_name_view', 'false'),
            'IsCancel' : params.get('is_cancel', 'true'),
            # 'UseMobilePin': params.get('use_mobie_pin', 'false')
        }

    def set_xml(self):
        try:
            Logger.logger.info("==== CouponInfo model set xml Start ====")
            Logger.logger.info("==== CouponInfo xml parsing ====")

            tree = ET.parse(os.path.join(xml_path, "coupon_info.xml"))

            root = tree.getroot()
            Logger.logger.info("==== CouponInfo API xml parsing success====")

            encTicket = root.find("soap:Header", self.namespace). \
                find('base:EncTicket', self.namespace). \
                find('base:encTicket', self.namespace)

            Logger.logger.info("==== CouponInfo API xml encTicket Setting Success ====")
            encTicket.text = encticket


            element_add_item_coupon = root.find('soap:Body', self.namespace). \
                find('base:AddItemCoupon', self.namespace). \
                find('base:AddItemCoupon', self.namespace)

            for key, value in self.add_item_coupon.items():
                Utils.set_xml_element_attrib(element_add_item_coupon, key, value)

            Logger.logger.info("==== CouponInfo API xml body setting Success ====")

        except BaseException as e:
            Logger.logger.info('CouponInfo Info create xml Failed')
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_coupon_regist)

        result = ET.tostring(root, encoding='utf8', method='xml')
        Logger.logger.info("==== CouponInfo API xml Success ====")
        Logger.logger.info(result.decode())
        return Utils().makeResponse(StrRepository().error_none, result)


class PriceInfo:
    namespace = {
        'soap': "http://schemas.xmlsoap.org/soap/envelope/",
        'base': "http://tpl.gmarket.co.kr/",
        'xsd': "http://tpl.gmarket.co.kr/tpl.xsd"
    }

    name = "AddPrice"

    def __init__(self, params):
        display_date = params.get('display_date') if params.get('display_date') is not None else params.get('expiration_date')
        Logger.logger.info('set PriceInfo')
        Logger.logger.info(params)
        try:
            if display_date is not None:
                expiration_date = str(display_date)
                display_date = expiration_date[:4] + '-' + expiration_date[4:6] + '-' + \
                                  expiration_date[6:]

        except BaseException as e:
            Logger.logger.info('set PriceInfo Failed')
            Logger.logger.info(e)

        self.add_price = {
            'GmktItemNo' : params.get('item_no'),
            'DisplayDate' : display_date,
            'StockQty' : params.get('stock_qty'),
            'SellPrice' : params.get('sell_price') if params.get('sell_price') is not None else params.get('price')
        }

    def set_xml(self):
        try:
            Logger.logger.info("==== PriceInfo model set xml Start ====")
            Logger.logger.info("==== PriceInfo xml parsing ====")

            tree = ET.parse(os.path.join(xml_path, "price_info.xml"))

            root = tree.getroot()
            Logger.logger.info("==== PriceInfo API xml parsing success====")

            encTicket = root.find("soap:Header", self.namespace). \
                find('base:EncTicket', self.namespace). \
                find('base:encTicket', self.namespace)

            Logger.logger.info("==== PriceInfo API xml encTicket Setting Success ====")
            encTicket.text = encticket

            element_add_price = root.find('soap:Body', self.namespace). \
                find('base:AddPrice', self.namespace). \
                find('base:AddPrice', self.namespace)

            for key, value in self.add_price.items():
                Utils.set_xml_element_attrib(element_add_price, key, value)

            Logger.logger.info("==== PriceInfo API xml body setting Success ====")

        except BaseException as e:
            Logger.logger.info('PriceInfo Info create xml Failed')
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_price_regist)

        result = ET.tostring(root, encoding='utf8', method='xml')
        Logger.logger.info("==== PriceInfo API xml Success ====")
        Logger.logger.info(result.decode())
        return Utils().makeResponse(StrRepository().error_none, result)


class PremiumInfo:
    namespace = {
        'soap': "http://schemas.xmlsoap.org/soap/envelope/",
        'base': "http://tpl.gmarket.co.kr/",
        'xsd': "http://tpl.gmarket.co.kr/tpl.xsd"
    }

    name = "AddPremiumItem"

    def __init__(self, params):
        self.item_no = params.get('item_no')

    def set_xml(self):
        try:
            Logger.logger.info("==== PremiumInfo model set xml Start ====")
            Logger.logger.info("==== PremiumInfo xml parsing ====")

            tree = ET.parse(os.path.join(xml_path, "premium_info.xml"))

            root = tree.getroot()
            Logger.logger.info("==== PremiumInfo API xml parsing success====")

            encTicket = root.find("soap:Header", self.namespace). \
                find('base:EncTicket', self.namespace). \
                find('base:encTicket', self.namespace)

            Logger.logger.info("==== PremiumInfo API xml encTicket Setting Success ====")
            encTicket.text = encticket

            element_premium = root.find('soap:Body', self.namespace). \
                find('base:AddPremiumItem', self.namespace). \
                find('base:AddPremiumItem', self.namespace)

            element_premium.attrib['GmktItemNo'] = self.item_no

            Logger.logger.info("==== PremiumInfo API xml body setting Success ====")

        except BaseException as e:
            Logger.logger.info('PremiumInfo Info create xml Failed')
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_premium_regist)

        result = ET.tostring(root, encoding='utf8', method='xml')
        Logger.logger.info("==== PremiumInfo API xml Success ====")
        Logger.logger.info(result.decode())
        return Utils().makeResponse(StrRepository().error_none, result)


class GmarketCategoryModel:
    GMARKET_CATEGORY_URL = "http://tpl.gmarket.co.kr/v1/Category/Category.xml"
    def fetch_categories_xml(self):
        response = None
        try:
            response = requests.get(self.GMARKET_CATEGORY_URL)
        except BaseException as e:
            Logger.logger.info("===== GMARKET_CATEGORY_REQUEST FAILD =====")
            Logger.logger.info(e)

        if response.code == 200:
            self.xml_categories = response.content
            return Utils().makeResponse(StrRepository().error_none)

        return Utils().makeResponse(StrRepository().error_system)

    def convert_xml_to_dict(self):
        pass



def gmarket_response(response_name, content):
    namespace = {
        'soap': "http://schemas.xmlsoap.org/soap/envelope/",
        'base': "http://tpl.gmarket.co.kr/",
    }

    tree = ET.ElementTree(ET.fromstring(content.decode()))
    root = tree.getroot()
    fault = root.find('soap:Body', namespace).find('soap:Fault', namespace)

    if fault is None:
        response = root.find('soap:Body', namespace).find('base:{}Response'.format(response_name), namespace).find('base:{}Result'.format(response_name), namespace)
        code = "00"
        result = response.attrib
    else:
        code = "-1"
        result = fault.find('faultstring').text

    return code, result



