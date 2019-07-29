angular.module('app.repository', [])

.constant('stringRepository', {
    IDS_ALERT_POPUP_INPUT_PHONENUM: '전화번호를 입력해 주세요.',
	IDS_ALERT_POPUP_INPUT_NOT_PHONENUM: '유효하지 않은 번호 입니다.',
    IDS_ALERT_POPUP_INPUT_BIRTHDAY: '생년월일 8자리를 입력해 주세요',
	IDS_ALERT_POPUP_ERROR_YEAR: '연도는 1900보다 커야합니다.',
    IDS_ALERT_POPUP_ERROR_MONTH: '월은 12보다 작아야 합니다.',
    IDS_ALERT_POPUP_ERROR_DAY: '일은 31보다 작아야 합니다.',
    IDS_ALERT_POPUP_INPUT_PASSWORD_NUM_CHARACTER: '비밀번호는 영문 숫자 혼합되어야 합니다.',
    IDS_ALERT_POPUP_INPUT_PASSWORD_LENGTH: '비밀번호는 영문숫자 조합 6자리 이상입니다.',
    IDS_ALERT_POPUP_INPUT_PASSWORD: '비밀번호가 일치 하지 않습니다.',
    IDS_ALERT_POPUP_INPUT_PASSWORD_CHECK: '비밀번호를 입력해 주세요.',
    IDS_ALERT_POPUP_INPUT_CHECK_EMAIL: '잘못된 이메일 형식입니다.'
});
