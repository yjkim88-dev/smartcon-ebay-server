'use strict';

/**
 * @ngdoc function
 * @name scmsApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the scmsApp
 */
angular.module('app.orderController', [])

.controller('orderController', function ($scope, $state, restFactory, usSpinnerService, errCheckFactory, $window) {
    console.log('orderController');
    console.log(sessionStorage.getItem('userId'));

    var now = new Date();

    $scope.model = {
        start_date: String(now.getFullYear()) + String(appendZero(now.getMonth() + 1))
                    + String(appendZero(now.getDate())),
        end_date: String(now.getFullYear()) + String(appendZero(now.getMonth() + 1))
                    + String(appendZero(now.getDate())),

        search_text: '',
        data_select: ''
    };

    $scope.resend_num = '';
    $scope.add_date = 0;

    $scope.orderList = [];

    // pagination start [
    $scope.filteredOrders = [];
    $scope.itemsPerPage = 10;
    $scope.currentPage = 1;

    $scope.figureOutOrdersToDisplay = function() {
        var begin = (($scope.currentPage - 1) * $scope.itemsPerPage);
        var end = begin + $scope.itemsPerPage;
        $scope.filteredOrders = $scope.orderList.slice(begin, end);
    };

    // $scope.makeTodos();
    // $scope.figureOutTodosToDisplay();

    $scope.pageChanged = function() {
        $scope.figureOutOrdersToDisplay();
    };
    // pagination end ]


    const pickerStart = datepicker(document.querySelector('#calendarStart'), {
        position: 'br', // Top right.
        startDate: new Date(), // This month.
        dateSelected: new Date(), // Today is selected.
        minDate: new Date(2010, 0, 1), // June 1st, 2016.
        maxDate: new Date(2099, 0, 1), // Jan 1st, 2099.
        noWeekends: false, // Weekends will be unselectable.
        formatter: function(el, date) {
            // This will display the date as `1/1/2017`.
            el.value = date.toDateString();
            console.log(el.value);
        },
        onSelect: function(instance) {
            // Show which date was selected.
            console.log(instance);

            var selectDate = new Date(instance.dateSelected);
            $scope.$apply(function() {
                $scope.model.start_date = String(selectDate.getFullYear()) + String(appendZero(selectDate.getMonth() + 1)) + String(appendZero(selectDate.getDate()));
            });

        },
        onShow: function(instance) {
            console.log('Calendar showing.');
        },
        onHide: function(instance) {
            console.log('Calendar hidden.');
        },
        onMonthChange: function(instance) {
            // Show the month of the selected date.
            console.log(instance.currentMonthName);
        },
        customMonths: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],
        customDays: ['일', '월', '화', '수', '목', '금', '토'],
        overlayPlaceholder: 'Enter a 4-digit year',
        overlayButton: '제출',
        disableMobile: true // Conditionally disabled on mobile devices.
    });

    const pickerEnd = datepicker(document.querySelector('#calendarEnd'), {
        position: 'br', // Top right.
        startDate: new Date(), // This month.
        dateSelected: new Date(), // Today is selected.
        minDate: new Date(2010, 0, 1), // June 1st, 2016.
        maxDate: new Date(2099, 0, 1), // Jan 1st, 2099.
        noWeekends: false, // Weekends will be unselectable.
        formatter: function(el, date) {
            // This will display the date as `1/1/2017`.
            el.value = date.toDateString();
        },
        onSelect: function(instance) {
            // Show which date was selected.
            console.log(instance);

            var selectDate = new Date(instance.dateSelected);
            $scope.$apply(function() {
                $scope.model.end_date = String(selectDate.getFullYear()) + String(appendZero(selectDate.getMonth() + 1)) + String(appendZero(selectDate.getDate()));
            });
        },
        onShow: function(instance) {
            console.log('Calendar showing.');
        },
        onHide: function(instance) {
            console.log('Calendar hidden.');
        },
        onMonthChange: function(instance) {
            // Show the month of the selected date.
            console.log(instance.currentMonthName);
        },
        customMonths: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],
        customDays: ['일', '월', '화', '수', '목', '금', '토'],
        overlayPlaceholder: 'Enter a 4-digit year',
        overlayButton: '제출',
        disableMobile: true // Conditionally disabled on mobile devices.
    });

    $scope.onClickOrder = function(order) {
        console.log('onClickOrder');
        $scope.detailOrder = order;

        console.log($scope.detailOrder);

        usSpinnerService.spin('spinner-1');

        var params = {
            tr_id: $scope.detailOrder.tr_id
        }

        restFactory.request(baseURL).all('resend').get('', params).then(function(res) {
            console.log(res)
            if (res.errorCode == '00') {
                $scope.resendInfo = res.results;
                angular.element(document.querySelector('#modalOrderDetail')).modal('show');
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

    $scope.onClickAddDate = function() {
        console.log('onClickAddDate');

        if ($scope.add_date < 0) {
            alert('연장 요청일은 0보다 커야 합니다.');
            return;
        }

        usSpinnerService.spin('spinner-1');

        console.log($scope.detailOrder);

        var params = {
            'tr_id' : $scope.detailOrder.tr_id,
            'event_id' : $scope.detailOrder.svc_event_id,
            'member_id' : $scope.detailOrder.member_id,
            'incre_exchange_day' : $scope.add_date
        }

        restFactory.request(baseURL).all('add_date').post(params).then(function(res) {
            console.log(res);

            if (res.errorCode == '00') {
                alert('유효기간 연장 완료 : ' + res.results[0].exchange_possible_enddate);
                //$scope.onGetOrderList();
                $scope.onUpdateState($scope.detailOrder);
                angular.element(document.querySelector('#modalOrderDetail')).modal('hide');
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

    $scope.onShowCancelOrder = function() {
        console.log('onClickCancelOrder');

        angular.element(document.querySelector('#modalCancelOrder')).modal('show');
    };

    $scope.onCancelOrder = function() {
        usSpinnerService.spin('spinner-1');

        var params = {
            'tr_id' : $scope.detailOrder.tr_id,
            'member_id' : $scope.detailOrder.member_id,
            'cancel_user' : sessionStorage.getItem('userId')
        };

        restFactory.request(baseURL).all('cancel').post(params).then(function(res) {
            console.log(res)
            if (res.errorCode == '00') {
                alert('주문 취소 완료');
                // $scope.onGetOrderList();
                $scope.onUpdateState($scope.detailOrder);
                angular.element(document.querySelector('#modalCancelOrder')).modal('hide');
                angular.element(document.querySelector('#modalOrderDetail')).modal('hide');
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

    $scope.onGetOrderList = function() {
        usSpinnerService.spin('spinner-1');

        restFactory.request(baseURL).all('orders').get('', $scope.model).then(function(res) {
            console.log(res)
            if (res.errorCode == '00') {
                $scope.orderList = res.results;
                $scope.figureOutOrdersToDisplay();
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

    $scope.onResend = function() {
        usSpinnerService.spin('spinner-1');

        restFactory.request(baseURL).all('resend').post($scope.resend_params).then(function(res) {
            console.log(res);
            if (res.errorCode == '00') {
                alert('재발송 성공');
                angular.element(document.querySelector('#modalResend')).modal('hide');
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

    $scope.onClickResend = function(order) {
        console.log('on resend');
        console.log(order);
        $scope.resend_phone = order.receiver_mobile;

        $scope.resend_params = {'comp_code': order.svc_event_id,
                    'cpn_no': order.svc_barcode_num,
                    'phone': order.receiver_mobile,
                    'callback': order.buyer_mobile,
                    'title': '',
                    'add_msg': '',
                    'tr_id': order.tr_id};

        angular.element(document.querySelector('#modalResend')).modal('show');
    };

    $scope.onClickResendNewNumber = function(order) {
        $scope.resendOrder = order;
        $scope.resend_num = '';
        angular.element(document.querySelector('#modalResendNewNumber')).modal('show');
    };

    $scope.onResendNew = function() {
        var checkPhone = errCheckFactory.checkPhoneNum($scope.resend_num);

        if (checkPhone == null) {
            //번호 변경 재발송
            usSpinnerService.spin('spinner-1');

            $scope.resend_params = {
                'comp_code': $scope.resendOrder.svc_event_id,
                'cpn_no': $scope.resendOrder.svc_barcode_num,
                'phone': $scope.resend_num,
                'callback': $scope.resendOrder.buyer_mobile,
                'title': '',
                'add_msg': '',
                'tr_id': $scope.resendOrder.tr_id
            };

            restFactory.request(baseURL).all('resend').post($scope.resend_params).then(function(res) {
                console.log(res);
                if (res.errorCode == '00') {
                    alert('재발송 성공');
                    // $scope.onGetOrderList();
                    $scope.onUpdateState($scope.detailOrder);
                    angular.element(document.querySelector('#modalResendNewNumber')).modal('hide');
                } else {
                    alert('error code : ' + res.errorCode + ', error message : ' + res.errorMsg);
                }
            }, function(response) {
                alert('connection error');
            }).finally(function() {
                console.log('finally');
                usSpinnerService.stop('spinner-1');
            });
        } else {
            alert(checkPhone);
        }
    };

    $scope.onUpdateState = function(order) {
        console.log('onUpdateState');

        usSpinnerService.spin('spinner-1');

        console.log(order);

        var params = {
            'tr_id': order.tr_id,
            'event_id': order.svc_event_id,
            'member_id': order.member_id,
            'send_no': order.send_no,
            'order_id': order.order_no
        };

        restFactory.request(baseURL).all('cp_state').post(params).then(function(res) {
            console.log(res);

            if (res.errorCode == '00') {
                order.exchange_status = res.results[0].exchange_status;
                order.claim_date = res.results[0].claim_date;
                order.valid_end = res.results[0].valid_end;
                order.claim_type = res.results[0].claim_type;
                order.send_status = res.results[0].send_status;
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

    $scope.onUpdateAll = function() {
        console.log('onUpdateAll');

        for (var i=0; i<$scope.filteredOrders.length; i++) {

            usSpinnerService.spin('spinner-1');

            var params = {
                'tr_id': $scope.filteredOrders[i].tr_id,
                'event_id': $scope.filteredOrders[i].svc_event_id,
                'member_id': $scope.filteredOrders[i].member_id,
                'send_no': $scope.filteredOrders[i].send_no,
                'order_id': $scope.filteredOrders[i].order_no
            };

            restFactory.request(baseURL).all('cp_state').post(params).then(function(res) {
                console.log(res);

                if (res.errorCode == '00') {
                    $scope.filteredOrders[i].exchange_status = res.results[0].exchange_status;
                    $scope.filteredOrders[i].claim_date = res.results[0].claim_date;
                    $scope.filteredOrders[i].valid_end = res.results[0].valid_end;
                    $scope.filteredOrders[i].claim_type = res.results[0].claim_type;
                    $scope.filteredOrders[i].send_status = res.results[0].send_status;
                } else {
                    alert('error code : ' + res.errorCode + ', error message : ' + res.errorMsg);
                }
            }, function(response) {
                alert('connection error');
            }).finally(function() {
                console.log('finally');
                usSpinnerService.stop('spinner-1');
            });
        }
    };

    $scope.onClickBarcode = function() {
        console.log('onClickBarcode');
        $window.open('http://211.43.202.132:17080/cs/list.hc', '_blank');

        // usSpinnerService.spin('spinner-1');
        //
        // var data = {
        //     "sCoupon_type": "S",
        //     "sBarcode_num": "012751410521"
        // };
        //
        // var data_encoded = $.param(data);
        //
        // console.log(data_encoded);
        //
        // restFactory.request("http://211.43.202.132:17080").all('cs/list.hc')
        //     .withHttpConfig({transformRequest: angular.identity})
        //     .customPOST(data_encoded, undefined, undefined, {'Content-Type': "x-www-form-urlencoded; charset=UTF-8"})
        //     .then(function(res) {
        //         console.log(res);
        //     }, function(response) {
        //         alert('connection error');
        //     }).finally(function() {
        //         console.log('finally');
        //         usSpinnerService.stop('spinner-1');
        //     });
    };

    $scope.onDownLoadExcel = function() {
        var data = [];
        console.log($scope.filteredOrders);

        for (var i=0; i<$scope.filteredOrders.length; i++) {
            var obj = {
                '채널 주문번호': $scope.filteredOrders[i].order_no,
                '채널 상품코드': $scope.filteredOrders[i].item_no,
                '상품명': $scope.filteredOrders[i].item_name,
                'B2C채널': $scope.filteredOrders[i].member_id,
                '주문자HP': $scope.filteredOrders[i].buyer_mobile,
                '수신자HP': $scope.filteredOrders[i].receiver_mobile,
                '연동코드': $scope.filteredOrders[i].out_item_no,
                'EVENT ID': $scope.filteredOrders[i].svc_event_id,
                '바코드 번호': $scope.filteredOrders[i].svc_barcode_num,
                '발송상태': $scope.filteredOrders[i].send_status,
                '발송요청일': $scope.filteredOrders[i].send_request_date,
                '발송완료일': $scope.filteredOrders[i].send_request_date,
                '교환상태': $scope.filteredOrders[i].exchange_status,
                '쿠폰상태': $scope.filteredOrders[i].claim_type
            }

            data.push(obj);
        }
        /* generate a worksheet */
        var ws = XLSX.utils.json_to_sheet(data);

        /* add to workbook */
        var wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "Sheet1");

        /* write workbook (use type 'binary') */
        var wbout = XLSX.write(wb, {bookType:'xls', type:'binary'});

        saveAs(new Blob([s2ab(wbout)],{type:"application/octet-stream"}), "주문내역조회.xls");
    };

})

.controller('resendController', function ($scope, $state, restFactory, usSpinnerService) {
    console.log('resend controller');
    $scope.model = {
        comp_code: null,
        cpn_no: null,
        phone: null,
        callback: null,
        title: null,
        add_msg: null
    };

    $scope.onResend = function(order) {
        usSpinnerService.spin('spinner-1');

        restFactory.request(baseURL).all('resend').post($scope.model).then(function(res) {
            console.log(res)
            if (res.errorCode == '00') {
                alert('재발송 성공');
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

