angular.module('app.commonService', [])

.factory('localstorage', function($window) {
    return {
        set: function(key, value) {
            $window.localStorage[key] = value;
        },
        get: function(key, defaultValue) {
            return $window.localStorage[key] || defaultValue;
        },
        setObject: function(key, value) {
            $window.localStorage[key] = JSON.stringify(value);
        },
        getObject: function(key) {
            if ($window.localStorage[key] == undefined || $window.localStorage[key] == 'undefined')
                return null;
            return JSON.parse($window.localStorage[key] || '{}');
        }
    }
})

.factory('errCheckFactory', function(stringRepository) {
    return {
        checkEmail: function(email) {
            console.log(email);
            if (email == null || email == '') {
                return stringRepository.IDS_ALERT_POPUP_INPUT_CHECK_EMAIL;
            }
        },
        checkPassword: function(password, confirmPassword) {
            var chk_num = null;
            var chk_eng = null;

            var idReg = /^[A-za-z0-9]{6,}$/g;

            if (password != null) {
                chk_num = password.search(/[0-9]/g);
                chk_eng = password.search(/[a-z]/ig);
            } else {
                return stringRepository.IDS_ALERT_POPUP_INPUT_PASSWORD_CHECK;
            }

            if (password != confirmPassword) {
                return stringRepository.IDS_ALERT_POPUP_INPUT_PASSWORD;
            } else if (!idReg.test(password)) {
                return stringRepository.IDS_ALERT_POPUP_INPUT_PASSWORD_LENGTH;
            } else if (chk_num < 0 || chk_eng < 0) {
                return stringRepository.IDS_ALERT_POPUP_INPUT_PASSWORD_NUM_CHARACTER;
            } else {
                return null;
            }
        },

        checkBirthday: function(birthday) {

            if (birthday != null) {
                birthday += '';
                if (birthday.length < 8) {
                    return stringRepository.IDS_ALERT_POPUP_INPUT_BIRTHDAY;
                } else {
                    var year = birthday.slice(0, 4);
                    var month = birthday.slice(4, 6);
                    var day = birthday.slice(6, 8);

                    if (Number(year) < 1900) {
                        return stringRepository.IDS_ALERT_POPUP_ERROR_YEAR;
                    } else if (Number(month) > 12) {
                        return stringRepository.IDS_ALERT_POPUP_ERROR_MONTH;
                    } else if (Number(day) > 31) {
                        return stringRepository.IDS_ALERT_POPUP_ERROR_DAY;
                    }
                }
            } else {
                return stringRepository.IDS_ALERT_POPUP_INPUT_BIRTHDAY;
            }

            return null;
        },

        checkPhoneNum: function(phoneNum) {
            console.log(phoneNum);

            if (phoneNum == null
                || phoneNum.length <= 0) {
                return stringRepository.IDS_ALERT_POPUP_INPUT_PHONENUM;
            } else {
                // 하이푼 제거
                console.log('phone number = ' + phoneNum);
                phoneNum = phoneNum.replace(/\-/g, '');
                phoneNum = phoneNum.replace('+82', '0')
                console.log('phone number = ' + phoneNum);

                // 체크
                if (phoneNum.length == 11 || phoneNum.length == 10) {
                    var regExp = /^01([016789])([1-9]{1})([0-9]{2,3})([0-9]{4})$/;

                    if (regExp.test(phoneNum)) {
                        console.log('phone number check OK');
                    } else {
                        return stringRepository.IDS_ALERT_POPUP_INPUT_NOT_PHONENUM;
                    }
                } else {
                    return stringRepository.IDS_ALERT_POPUP_INPUT_NOT_PHONENUM;
                }

                return null;
            }
        }
    }
})

.factory('userService', function() {
    // 로그인 유저 데이터
    var userInfo = {
        id: null,
        phoneNum: null,
        uuid: null,
        authKey: null,
        userToken: null,
        pushToken: null,
        userName: null
    }

    // 서버에서 조회한 유저 데이터
    var restUserInfo = null;

    return {
        all: function() {
            return userInfo;
        },
        setUserId: function(_id) {
            userInfo.id = _id;
        },
        getUserId: function() {
            return userInfo.id;
        },
        setPhoneNum: function(_phoneNum) {
            userInfo.phoneNum = _phoneNum;
        },
        getPhoneNum: function() {
            return userInfo.phoneNum;
        },
        setUUID: function(_uuid) {
            userInfo.uuid = _uuid;
        },
        getUUID: function() {
            return userInfo.uuid;
        },
        setAuthKey: function(_authKey) {
            userInfo.authKey = _authKey;
        },
        getAuthKey: function() {
            return userInfo.authKey;
        },
        setUserToken: function(_userToken) {
            userInfo.userToken = _userToken;
        },
        getUserToken: function() {
            return userInfo.userToken;
        },
        setRestUserInfo: function(_userInfo) {
            restUserInfo = _userInfo;
        },
        getRestUserInfo: function() {
            return restUserInfo;
        },
        getUserStampCount: function() {
            return restUserInfo.stamp_cnt;
        },
        getUserCash: function() {
            return restUserInfo.use_able_cash;
        },
        setPushToken: function(token) {
            userInfo.pushToken = token;
        },
        getPushToken: function() {
            return userInfo.pushToken;
        },
        setUserName: function(_userName) {
            userInfo.userName = _userName;
        },
        getUserName: function() {
            return userInfo.userName;
        }
    };
});