'use strict';

/**
 * @ngdoc function
 * @name scmsApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the scmsApp
 */
angular.module('app.blacklistController', [])

.controller('blacklistSearchController', function ($scope, $state, restFactory, usSpinnerService) {
    console.log('blacklistSearchController')

    $scope.blacklist = [];

    $scope.model = {
        phone_num: ''
    };

    $scope.modal = {
        phone_num: null,
        reason: null
    };


    $scope.onGetBlackList = function() {
        usSpinnerService.spin('spinner-1');

        restFactory.request(baseURL).all('blacklist').get('', {'phone_num': $scope.model.phone_num.replace(/-/g, "")}).then(function(res) {
            console.log(res)
            if (res.errorCode == '00') {
                $scope.blacklist = res.results;
            } else {
                alert('error code : ' + res.errorCode + ', error message : ' + res.errorMsg);
            }
        }, function(response) {
            alert('connection error');
        }).finally(function() {
            console.log('finally');
            usSpinnerService.stop('spinner-1');
        });
    };

    $scope.onClickList = function(item) {
        console.log(item);

        $scope.modal.phone_num = item.phone_num;
        $scope.modal.reason = item.reason;
        angular.element(document.querySelector('#modalDetail')).modal('show');
    };

    $scope.onUpdate = function() {
        restFactory.request(baseURL).all('blacklist').customPUT({'phone_num': $scope.modal.phone_num.replace(/-/g, ""),
                                                                'reason': $scope.modal.reason}).then(function(res) {
            console.log(res)
            if (res.errorCode == '00') {
                alert('수정 되었습니다.');
                angular.element(document.querySelector('#modalDetail')).modal('hide');

                $scope.onGetBlackList();
            } else {
                alert('error code : ' + res.errorCode + ', error message : ' + res.errorMsg);
            }
        }, function(response) {
            alert('connection error');
        }).finally(function() {
            console.log('finally');
            usSpinnerService.stop('spinner-1');
        });
    };

    $scope.onDelete = function() {
        restFactory.request(baseURL).all('blacklist').customDELETE('', {'phone_num': $scope.modal.phone_num.replace(/-/g, "")}).then(function(res) {
            console.log(res)
            if (res.errorCode == '00') {
                alert('삭제 되었습니다.');
                angular.element(document.querySelector('#modalDetail')).modal('hide');

                $scope.onGetBlackList();
            } else {
                alert('error code : ' + res.errorCode + ', error message : ' + res.errorMsg);
            }
        }, function(response) {
            alert('connection error');
        }).finally(function() {
            console.log('finally');
            usSpinnerService.stop('spinner-1');
        });
    };

})

.controller('blacklistRegistController', function ($scope, restFactory, usSpinnerService) {
    console.log('blacklistRegistController')

    $scope.blacklist = [];

    $scope.model = {
        phone_num: null,
        reason: ''
    }

    $scope.onRegistBlackList = function() {
        usSpinnerService.spin('spinner-1');

        if ($scope.model.phone_num == '' || $scope.model.phone_num == null) {
            alert('전화번호를 입력해 주세요');
            usSpinnerService.stop('spinner-1');
            return;
        }

        restFactory.request(baseURL).all('blacklist').post({'phone_num': $scope.model.phone_num.replace(/-/g, ""),
                                                            'reason': $scope.model.reason,
                                                            'user_id': sessionStorage.getItem('userId')}).then(function(res) {
            console.log(res)
            if (res.errorCode == '00') {
                alert('등록 되었습니다.');

                $scope.model.phone_num = null;
                $scope.model.reason = '';

            } else {
                alert('error code : ' + res.errorCode + ', error message : ' + res.errorMsg);
            }
        }, function(response) {
            alert('connection error');
        }).finally(function() {
            console.log('finally');
            usSpinnerService.stop('spinner-1');
        });
    };

})



