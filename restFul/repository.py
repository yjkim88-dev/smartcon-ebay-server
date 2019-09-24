#_*_ coding: utf-8 _*_

class StrRepository:
    def __init__(self):
        self.error_none = '00', ''
        self.error_input_order_date = '99', '날짜를 입력 해주세요'
        self.error_order_type = '98', '조회 날짜 형식은 yyyymmdd입니다.'
        self.error_resend_count = '97', '재전송 횟수 초과 입니다.'
        self.error_goods_regist = '96', '상품 등록에 실패 했습니다.'
        self.error_official_regist = '95', '고시정보 등록에 실패 했습니다.'
        self.error_coupon_regist = '94', '쿠폰정보 등록에 실패 했습니다.'
        self.error_coupon_regist_db = '94-1', 'DB에 없는 쿠폰정보입니다.'
        self.error_price_regist = '93', '가격정보 등록에 실패 했습니다.'
        self.error_premium_regist = '92', '가격정보 등록에 실패 했습니다.'
        self.error_already_regist = '91', '이미 블랙리스트에 등록된 사용자 입니다.'
        self.error_nothing_blacklist = '90', '블랙리스트에 등록된 사용자가 없습니다.'
        self.error_nothing_goods = '89', '등록된 상품이 없습니다.'
        self.error_check_user_password = '88', '사용자 ID 및 비밀 번호를 확인하세요.'
        self.error_not_found_send = '87', '발송 내역이 존재하지 않습니다.',
        self.error_not_add_date = '86', '유효기간 연장 실패.',
        self.error_send_state_update = '85', '발송 상태 업데이트 실패',
        self.error_exchange_state_update = '84', '교환 상태 업데이트 실패',

        self.error_system = '100', '시스템오류 필수 파라메터 확인 및 관리자에게 문의 해주세요'
        self.error_duplicate = '101', '중복입력 오류'

        self.error_auth = '401', '인증키가 올바르지 않습니다.'

        self.error_gmkt_network = '502', '네트워크 에러가 발생했습니다. 지마켓 등록번호 확인 후 (등록/수정) 재시도 바랍니다.'
        self.success_gmkt_excel_upload = '00', '성공적으로 등록되었습니다.'
        # 이지웰 상품등록
        self.error_ezwel_goods = '50', '상품 등록 오류'
        self.error_ezwel_goods_image = '51', '상품 이미지 등록 오류'
        self.error_ezwel_goods_shop = '52', '상품 매장 등록 오류'
        self.error_ezwel_goods_pin = '53', '핀 정보 등록 오류'
        self.error_ezwel_end_date = '54', '유효기간 종료일을 입력해주세요'
        self.error_ezwel_end_date_count = '55', '발급일 이후 유효기간을 입력해주세요'

