from .gmarket_api_models import AddItem, OfficialInfo, CouponInfo, PriceInfo, PremiumInfo
from restFul.v2.gmarket.goods_regist_dao import GoodsRegistDao
from restFul.v2.gmarket.gmarket_api import GmarketAPI
from restFul.repository import StrRepository
from restFul.utils import Utils
from Logger import Logger
from restFul.util_services.excel_service import ExcelGeneratorV2


class GmarketGoodsService:
    api_url_add_item = 'http://tpl.gmarket.co.kr/v1/ItemService.asmx'
    headers = {'Content-Type': 'text/xml; charset=utf-8'}

    @classmethod
    def mysql_fetch_goods(cls, params):
        try:
            item_no = params['item_no']
            result = GoodsRegistDao().fetch_goods(item_no)
            if result.get('errorCode') != "00":
                return result
        except BaseException as e:
            Logger.logger.info('goods service faild')
            Logger.logger.waring(e)
            return Utils().makeResponse(StrRepository().error_system)
        return result

    @classmethod
    def mysql_fetch_goods_list_(cls, params):
        try:
            result = GoodsRegistDao().selectGoods(params.get('start_date'), params.get('end_date'),
                                                  params.get('item_no'))
            if result.get('errorCode') != "00":
                return result
        except BaseException as e:
            Logger.logger.info('mysql_fetch_goods_list_faild')
            Logger.logger.waring(e)
            return Utils().makeResponse(StrRepository().error_system)
        return result

    @classmethod
    def mysql_fetch_goods_list(cls):
        try:
            result = GoodsRegistDao().fetch_goods_list_coupon()
            if result.get('errorCode') != "00":
                return result
        except BaseException as e:
            Logger.logger.info('goods service faild')
            Logger.logger.waring(e)
            return Utils().makeResponse(StrRepository().error_system)
        return result

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
            add_item_api = GmarketAPI(item_model)  # 이베이 쿠폰등록 인스턴스 생성
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
            add_official_info_api = GmarketAPI(official_info_model)
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
            add_coupon_info_api = GmarketAPI(coupon_info_model)
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
            add_price_api = GmarketAPI(price_info_model)
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
            add_premium_api = GmarketAPI(premium_info_model)
            add_premium_api_result = add_premium_api.run()
        except BaseException as e:
            Logger.logger.info("=========== ERROR PREMIUM API ===========")
            Logger.logger.info(e)
            return Utils().makeResponse(StrRepository().error_system)
        return add_premium_api_result


class GmarketExcelDownloadService:
    @classmethod
    def create_goods_infos_excel(cls, goods_infos):
        goods_info_key = [
            'ITEM_NO', 'ITEM_NAME', 'PRICE', 'OUT_ITEM_NO', 'STOCK_QTY', 'EXPIRATION_DATE', 'AUTO_TERM_DURATION',
            'AUTO_USE_TERM_DURATION', 'DEFAULT_IMAGE', 'APPLY_PLACE', 'APPLY_PLACE_URL', 'APPLY_PLACE_TELEPHONE',
            'USE_INFORMATION', 'HELP_DESK_TELNO', 'CREATE_DATE', 'MODIFY_DATE'
        ]

        goods_info_header = [
            '지마켓 상품코드', '상품명', '정상가', '연동코드', '재고수량', '상품 만료일', '정산기간', '유효기간', '상품 이미지 URL',
            '사용장소', '사용장소 URL', '사용장소 전화번호', '사용 유의사항', '고객센터', '등록일', '수정일'
        ]

        goods_info_style = {
            'ITEM_NO': 'string',
            'ITEM_NAME': 'string',
            'PRICE': 'cash',
            'OUT_ITEM_NO': 'string',
            'STOCK_QTY': 'cash',
            'EXPIRATION_DATE': 'date',
            'AUTO_TERM_DURATION': 'string',
            'AUTO_USE_TERM_DURATION': 'string',
            'DEFAULT_IMAGE': 'string',
            'APPLY_PLACE': 'string',
            'APPLY_PLACE_URL': 'string',
            'APPLY_PLACE_TELEPHONE': 'string',
            'USE_INFORMATION': 'string',
            'HELP_DESK_TELNO': 'string',
            'CREATE_DATE': 'date',
            'MODIFY_DATE': 'date'
        }

        excel = ExcelGeneratorV2("지마켓 상품정보")
        excel.set_page(1)

        excel.set_header(goods_info_key, goods_info_header)
        excel.set_field(goods_infos, 1)
        excel.set_field_format(goods_info_style)
        excel.set_header_opt({})

        excel.write_excel()

        return excel.get_xlsx_path()

    @classmethod
    def create_coupon_infos_excel(cls, CouponInfo):
        cus_key = [
            'item_no', 'item_name', 'use_information', 'default_image', 'apply_place', 'apply_place_url',
            'apply_place_telephone', 'price',
            'help_desk_telno', 'valid_term_type', 'auto_term_start_day', 'auto_term_duration', 'fixed_term_start_date',
            'fixed_term_end_date', 'use_term_type', 'auto_use_term_start_day', 'auto_use_term_duration',
            'fixed_use_term_start_date', 'fixed_use_term_end_date', 'publication_corp',
            'publication_corp_web_url', 'find_guide'
        ]

        cus_header = [
            '지마켓 상품코드', '상품명', '사용 유의 사항', '쿠폰이미지', '사용처', '사용처 URL', '사용처 전화번호', '가격', '고객센터', '정산기간 타입',
            '정산시작일', '쿠폰 정산기간', '정산특정시작날짜', '정산특정종료날짜', '유효기간 타입', '유효기간시작일', '쿠폰 유효기간', '유효특정시작날짜', '유효특정종료날짜',
            '발행업체', '발행업체웹페이지주소', '찾아가는 길'
        ]

        cus_format = {
            'item_no': 'string',
            'item_name': 'string',
            'apply_place_telephone': 'string',
            'use_information': 'string',
            'default_image': 'string',
            'apply_place': 'string',
            'apply_place_url': 'string',
            'price': 'string',
            'help_desk_telno': 'string',
            'coupon_type': 'string',
            'coupon_money_type': 'string',
            'valid_term_type': 'string',
            'auto_term_start_day': 'string',
            'auto_term_duration': 'string',
            'fixed_term_start_date': 'string',
            'fixed_term_end_date': 'string',
            'use_term_type': 'string',
            'auto_use_term_start_day': 'string',
            'auto_use_term_duration': 'string',
            'fixed_use_term_start_date': 'string',
            'fixed_use_term_end_date': 'string',
            'is_customer_name_view': 'string',
            'publication_corp': 'string',
            'publication_corp_web_url': 'string',
            'find_guide': 'string'
        }

        excel = ExcelGeneratorV2('coupon_info', False)
        excel.set_page(1)

        # 회원정보 입력
        excel.set_header(cus_key, cus_header)
        excel.set_field(CouponInfo, 1)
        excel.set_field_format(cus_format)
        excel.set_header_opt({})

        excel.write_excel()
        return excel.get_xlsx_path()
