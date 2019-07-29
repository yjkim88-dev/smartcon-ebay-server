'use strict';

/**
 * @ngdoc function
 * @name scmsApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the scmsApp
 */
angular.module('app.pagesController', [])

.controller('loginController', function ($scope, $state, usSpinnerService, restFactory) {
    console.log('loginController');
    // console.log(uuid.v4());

    $scope.model = {
        id: null,
        password: null
    };

    $scope.onLogin = function() {

        if ($scope.model.id == null || $scope.model.id == '') {
            alert ('id를 입력하세요');
            return;
        }

        if ($scope.model.password == null || $scope.model.password == '') {
            alert ('비밀번호를 입력하세요');
            return;
        }
        usSpinnerService.spin('spinner-1');

        // 공개키를 가져온다
        // restFactory.request(baseURL).all('generatekey').get('').then(function(res) {
        //     console.log(res);
        //     console.log(window.atob(``));
        //
        //     var encrypt = new JSEncrypt();
        //     encrypt.setPublicKey(res.public_key);
        //
        //     console.log('set pub');
        //     var params = {
        //         enc_id: $scope.model.id,
        //         enc_password: $scope.model.password
        //     };
        //
        //     console.log(params);
        //     params.enc_id = encrypt.encrypt(params.enc_id);
        //     params.enc_password = encrypt.encrypt(params.enc_password);
        //
        //     console.log(params);
        //
        //     restFactory.request(baseURL).all('login').post(params).then(function(res) {
        //         console.log(res)
        //         if (res.errorCode == '00') {
        //             $state.go('app.main');
        //         } else {
        //             alert('error code : ' + res.errorCode + ', error message : ' + res.errorMsg);
        //         }
        //     }, function(response) {
        //         alert('connection error');
        //     }).finally(function() {
        //         console.log('finally');
        //         usSpinnerService.stop('spinner-1');
        //     });
        //
        // }, function(response) {
        //     alert('connection error');
        // }).finally(function() {
        //     console.log('finally');
        //     usSpinnerService.stop('spinner-1');
        // });

        restFactory.request(baseURL).all('login').post($scope.model).then(function(res) {
            console.log(res)
            if (res.errorCode == '00') {
                console.log(res.results[0].auth_token);

                sessionStorage.setItem('token', res.results[0].auth_token);
                sessionStorage.setItem('userId', $scope.model.id);

                $state.go('app.main');
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
});
