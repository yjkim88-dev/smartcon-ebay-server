import html
import requests

from Logger import Logger
from .goods_regist_dao import GoodsRegistDao
from .gmarket_api_models import AddItem, OfficialInfo, CouponInfo, PriceInfo, PremiumInfo, gmarket_response
from restFul.repository import StrRepository
from restFul.utils import Utils
from restFul.v2.gmarket.gmarket_reg_api import GmarketRegAPI

class GmarketGoodsService:
    api_url_add_item = 'http://tpl.gmarket.co.kr/v1/ItemService.asmx'
    headers = {'Content-Type': 'text/xml; charset=utf-8'}

    # @classmethod
    # def goods_api(cls, params):
    #     try:
    #         # STEP1 상품등록
    #         item_model = AddItem(params)                        # 요청할 API 모델 생성
    #         add_item_api = GmarketRegAPI(item_model)         # 이베이 쿠폰등록 인스턴스 생성
    #         add_item_result = add_item_api.run()                # API 작업 수행
    #
    #         if add_item_result.get('errorCode') != "00":        # 작업 결과 확인
    #             return add_item_result                          # 에러 발생
    #         params['item_no'] = add_item_result.get('results')  # 상품 등록/수정 후 받은 지마켓 상품코드 적용
    #
    #         # STEP2 고시정보 등록
    #         official_info_model = OfficialInfo(params)
    #         add_official_info_api = GmarketRegAPI(official_info_model)
    #         add_official_info_result = add_official_info_api.run()
    #
    #         if add_official_info_result.get('errorCode') != "00":
    #             return add_official_info_result
    #
    #         # STEP3 쿠폰정보 등록
    #         coupon_info_model = CouponInfo(params)
    #         add_coupon_info_api = GmarketRegAPI(coupon_info_model)
    #         add_coupon_info_result = add_coupon_info_api.run()
    #
    #         if add_coupon_info_result.get('errorCode') != "00":
    #             return add_coupon_info_result
    #
    #         # STEP4 가격정보 등록
    #         price_info_model = PriceInfo(params)
    #         add_price_api = GmarketRegAPI(price_info_model)
    #         add_price_api_result = add_price_api.run()
    #
    #         if add_price_api_result.get('errorCode') != "00":
    #             return add_price_api_result
    #
    #         # STEP5 고객 혜택
    #         premium_info_model = PremiumInfo(params)
    #         add_premium_api = GmarketRegAPI(premium_info_model)
    #         add_premium_api_result = add_premium_api.run()
    #
    #         if add_premium_api_result.get('errorCode') != "00":
    #             return add_premium_api_result
    #     except BaseException as e:
    #         Logger.logger.info("=========== ERROR POST EXCEL GOODS ===========")
    #         Logger.logger.info(e)
    #         return Utils().makeResponse(StrRepository().error_system)
    #     return Utils().makeResponse(StrRepository().error_none)

    @classmethod
    def goods_api(cls, params):
        market_result = cls.market_api(params)
        if market_result.get('errorCode') != "00":
            return market_result

        try:
            params['item_no'] = market_result['results']
        except BaseException as e:
            Logger.logger.error('=== goods api ===')
            Logger.logger.error(e)
            return Utils().makeResponse(StrRepository().error_goods_regist)

        official_result = cls.official_api(params)
        if official_result.get('errorCode') != "00":
            return official_result

        coupon_market_result = cls.coupon_market_api(params)
        if coupon_market_result.get('errorCode') != "00":
            return coupon_market_result

        price_result = cls.price_api(params)
        if price_result.get('errorCode') != "00":
            return price_result

        premium_result = cls.premium_api(params)
        if premium_result.get('errorCode') != "00":
            return premium_result

        return Utils().makeResponse(StrRepository().error_none)

    @classmethod
    def market_api(cls, params):
        try:
            # STEP1 상품등록
            item_model = AddItem(params)  # 요청할 API 모델 생성
            add_item_api = GmarketRegAPI(item_model)  # 이베이 쿠폰등록 인스턴스 생성
            add_item_result = add_item_api.run()  # API 작업 수행

            if add_item_result.get('errorCode') != "00":  # 작업 결과 확인
                return add_item_result  # 에러 발생

        except BaseException as e:
            Logger.logger.info("=========== ERROR MARKET API ===========")
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)
        return add_item_result

    @classmethod
    def official_api(cls, params):
        try:
            # STEP2 고시정보 등록
            official_info_model = OfficialInfo(params)
            add_official_info_api = GmarketRegAPI(official_info_model)
            add_official_info_result = add_official_info_api.run()

            if add_official_info_result.get('errorCode') != "00":
                return add_official_info_result
        except BaseException as e:
            Logger.logger.info("=========== ERROR OFFICIAL API ===========")
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)
        return add_official_info_result

    @classmethod
    def coupon_market_api(cls, params):
        try:
            # STEP3 쿠폰정보(쿠폰마켓) 등록
            coupon_info_model = CouponInfo(params)
            add_coupon_info_api = GmarketRegAPI(coupon_info_model)
            add_coupon_info_result = add_coupon_info_api.run()

            if add_coupon_info_result.get('errorCode') != "00":
                return add_coupon_info_result
        except BaseException as e:
            Logger.logger.info("=========== ERROR COUPON MARKET API ===========")
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)
        return add_coupon_info_result

    @classmethod
    def price_api(cls, params):
        try:
            # STEP4 가격정보 등록
            price_info_model = PriceInfo(params)
            add_price_api = GmarketRegAPI(price_info_model)
            add_price_api_result = add_price_api.run()

            if add_price_api_result.get('errorCode') != "00":
                return add_price_api_result
        except BaseException as e:
            Logger.logger.info("=========== ERROR PRICE API ===========")
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)
        return add_price_api_result

    @classmethod
    def premium_api(cls, params):
        try:
            # STEP5 고객 혜택
            premium_info_model = PremiumInfo(params)
            add_premium_api = GmarketRegAPI(premium_info_model)
            add_premium_api_result = add_premium_api.run()
        except BaseException as e:
            Logger.logger.info("=========== ERROR PREMIUM API ===========")
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)
        return add_premium_api_result