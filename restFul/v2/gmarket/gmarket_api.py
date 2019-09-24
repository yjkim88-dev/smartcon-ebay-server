import requests
import html

from Logger import Logger
from restFul.utils import Utils
from restFul.repository import StrRepository
from restFul.v2.gmarket.gmarket_api_models import gmarket_response
from restFul.v2.gmarket.goods_regist_dao import GoodsRegistDao


class GmarketAPI:
    api_url_add_item = 'http://tpl.gmarket.co.kr/v1/ItemService.asmx'

    namespace = {
        'soap': "http://schemas.xmlsoap.org/soap/envelope/",
        'base': "http://tpl.gmarket.co.kr/",
    }

    headers = {'Content-Type': 'text/xml; charset=utf-8'}

    api_error = {
        'AddItem' : StrRepository().error_goods_regist,
        'AddOfficialInfo' : StrRepository().error_official_regist,
        'AddItemCoupon' : StrRepository().error_coupon_regist,
        'AddPrice' : StrRepository().error_price_regist,
        'AddPremiumItem' : StrRepository().error_premium_regist,
        'none' : StrRepository().error_none,
        'system' : StrRepository().error_system
    }

    def __init__(self, instance_model):
        self.model = instance_model
        self.name = instance_model.name
        self.make_response_data = Utils().makeResponse

    # API 통신 수행
    def run(self):
        xml_result = self.__set_xml_data()          # 모델 set_xml 메서드를 사용해 xml 데이터 설정
        if xml_result.get('errorCode') != "00":
            return xml_result

        ebay_result = self.__post_ebay()            # xml 데이터를 이베이측에 전송
        if ebay_result.get('errorCode') != "00":
            return ebay_result
        
        parsing_result = self.__parsing_response()  # 응답값 확인
        if parsing_result.get('errorCode') != "00":
            return parsing_result

        db_result = self.__database_process()       # DB 작업
        if db_result.get('errorCode') != "00":
            return db_result

        if self.name == 'AddItem':
            return self.make_response(True, self.model.add_item.get('GmktItemNo'))
        return self.make_response(True)

    def __set_xml_data(self):   # XML 데이터 생성
        self.title_logging("STEP1 GEN XML")
        try:
            result = self.model.set_xml()
            if result.get('errorCode') != "00":
                return result
            self.xml = result.get('results')
        except BaseException as e:
            self.title_logging("FAILD GEN XML")
            Logger.logger.info(e)
            return self.make_response(False)
        self.title_logging('SUCCESS GEN XML')
        Logger.logger.info(self.xml)
        return self.make_response(True)

    def __post_ebay(self):  # 이베이 post 요청
        self.title_logging('STEP2 POST REQUEST EBAY')
        try:
            self.response = requests.post(
                url=self.api_url_add_item,
                headers=self.headers,
                data=self.xml
            )
        except BaseException as e:
            self.title_logging('FALID POST REQUEST EBAY')       # 실패하는 경우
            Logger.logger.info(e)
            return self.make_response(False)
        self.title_logging('SUCCESS REQUEST EBAY')
        return self.make_response_data(self.api_error.get('none'))
    
    def __parsing_response(self):   # 응답값 파싱
        self.title_logging('STEP3 PARSING RESPONSE')
        item_no = None
        if self.name == "AddOfficialInfo":
            item_no = self.model.item_no
        elif self.name == "AddItemCoupon":
            item_no = self.model.add_item_coupon.get('GmktItemNo')
        elif self.name == "AddPrice":
            item_no = self.model.add_price.get('GmktItemNo')
        elif self.name == "AddPremiumItem":
            item_no = self.model.item_no
        try:
            if self.response.status_code != 200:

                return self.make_response_data(StrRepository().error_gmkt_network, item_no)

            code, result = gmarket_response(self.name, self.response.content)       # 응답 XML 파싱

            if code != "00":                            # 요청 실패
                self.title_logging('ERROR RESPONSE')
                Logger.logger.info(html.escape(result))
                return self.make_response(False, item_no)

            if result.get('Result') == 'Fail':          # 특정 값 에러
                self.title_logging("ERROR RESPONSE")
                Logger.logger.info(html.escape(result.get('Comment')))
                return self.make_response(False, item_no)

            if self.name == "AddItem":                          # AddItem인 경우 추가 작업
                item_no = result.get('GmktItemNo')              # 지마켓 상품 번호 업데이트
                group_code = result.get('ShippingGroupCode')    # 그룹코드 업데이트
                self.model.add_item['GmktItemNo'] = item_no
                self.model.shipping['GroupCode'] = group_code \
                    if group_code is not None \
                    else self.model.shipping.get('GroupCode')

        except BaseException as e:                          # 파싱 실패
            self.title_logging('FAILD PARSING RESPONSE')
            Logger.logger.info(e)
            return self.make_response(False, item_no)

        self.title_logging("SUCCESS PARSING RESPONSE")
        Logger.logger.info(result)
        return self.make_response(True, item_no)

    def __database_process(self):                           # 데이터베이스 적용
        self.title_logging('STEP4 DB TASK')
        try:
            if self.name == "AddItem":
                add_item_result = GoodsRegistDao().goods_market_info_db_service(self.model.add_item.get('GmktItemNo'), self.model, self.model.user_id)
                if add_item_result.get('errorCode') != "00":
                    return add_item_result
                self.title_logging('SUCCESS DB TASK')
            elif self.name == "AddOfficialInfo":
                official_result = GoodsRegistDao().update_goods_sub_official_info(self.model)
                if official_result.get('errorCode') != "00":
                    return official_result
            elif self.name == "AddItemCoupon":
                coupon_result = GoodsRegistDao().update_goods_coupon_info(self.model)
                if coupon_result.get('errorCode') != "00":
                    return coupon_result
                self.title_logging('SUCCESS DB TASK')
            elif self.name == "AddPrice":
                price_result = GoodsRegistDao().update_goods_price_info(self.model)
                if price_result.get('errorCode') != "00":
                    return price_result
                self.title_logging('SUCCESS DB TASK')
            else:
                self.title_logging('STEP4 DB TASK PASS')
        except BaseException as e:
            self.title_logging('FAILD DB TASK')
            Logger.logger.info(e)
            return self.make_response(False)
        return self.make_response(True)

    # 메서드 결과 리턴
    def make_response(self, isSuccess, value=None):
        try:
            errors = self.api_error['none'] if isSuccess else self.api_error[self.name]
        except BaseException as e:
            return self.make_response_data(self.api_error.get('system'))
        return self.make_response_data(errors, value)
    # 로깅 래핑

    def title_logging(self, text):
        Logger.logger.info("===== {} {} =====".format(self.name, text))