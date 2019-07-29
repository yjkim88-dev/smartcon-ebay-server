'use strict';

/**
 * @ngdoc function
 * @name scmsApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the scmsApp
 */
angular.module('app.goodsController', [])

.controller('goodsSearchController', function ($scope, $state, restFactory, usSpinnerService, $sce) {
    console.log('goodsSearchController')

    var now = new Date();

    $scope.model = {
        start_date: String(now.getFullYear()) + String(appendZero(now.getMonth() + 1))
                    + String(appendZero(now.getDate())),
        end_date: String(now.getFullYear()) + String(appendZero(now.getMonth() + 1))
                    + String(appendZero(now.getDate())),
        item_no: null
    };

    // pagination start [
    $scope.goodsList = [];
    $scope.filteredOrders = [];
    $scope.itemsPerPage = 10;
    $scope.currentPage = 1;

    $scope.figureOutOrdersToDisplay = function() {
        var begin = (($scope.currentPage - 1) * $scope.itemsPerPage);
        var end = begin + $scope.itemsPerPage;
        $scope.filteredOrders = $scope.goodsList.slice(begin, end);
    };

    $scope.pageChanged = function() {
        $scope.figureOutOrdersToDisplay();
    };
    // pagination end ]

    $scope.renderHtml = function(htmlCode) {
        if (typeof(htmlCode) != 'undefined') {
  	    htmlCode.replace(/img/gi, "img style=width:100%;");
            return $sce.trustAsHtml(htmlCode);
        }
    };

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
            console.log(el.value);
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

    $scope.onSearchGoods = function() {
        usSpinnerService.spin('spinner-1');

        restFactory.request(baseURL).all('goods').get('', $scope.model).then(function(res) {
            console.log(res)
            if (res.errorCode == '00') {
                $scope.goodsList = res.results;
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

    $scope.onClickList = function(item) {
        console.log(item);
        $scope.modalitem = item;
        $scope.modalitem.gd_html = $scope.modalitem.gd_html.replace(/img/gi, "img style=width:100%;");

        console.log($scope.modalitem.gd_html);
        angular.element(document.querySelector('#modalGoodsDetail')).modal('show');
    };
})

.controller('goodsRegistController', function ($scope, $state, restFactory, usSpinnerService, Upload) {
    console.log('goodsRegistController');
    var now = new Date();

    $scope.model = {
        expiration_date: String(now.getFullYear()) + String(appendZero(now.getMonth() + 1))
                    + String(appendZero(now.getDate())),
        event_id: null,
        out_item_no: null,
        category_code: null, //'300020076',
        item_no: null,
        item_name: null,
        gd_html: null,
        maker_no: '201171998', // bhc: '1998847', //'201171998',
        brand_no: null,
        price: null,
        help_desk_telno: '02-561-0671',
        auto_term_duration: 7,
        auto_use_term_duration: null,
        apply_place: null,
        apply_place_url: null,
        apply_place_telephone: null,
        stock_qty: null,
        use_information: null,
        brand_name: null,
        default_image: null,
        user_id: sessionStorage.getItem('userId')
    }

    const pickerStart = datepicker(document.querySelector('#calendarExpired'), {
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
                $scope.model.expiration_date = String(selectDate.getFullYear()) + String(appendZero(selectDate.getMonth() + 1)) + String(appendZero(selectDate.getDate()));
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

    $scope.onRegistGoods = function() {
        if ($scope.model.event_id == null || $scope.model.event_id == '') {
            alert('이벤트 ID를 입력하세요.');
            return;
        }
        if ($scope.model.out_item_no == null || $scope.model.out_item_no == '') {
            alert('스마트콘 연동 코드를 입력하세요.');
            return;
        }
        if ($scope.model.category_code == null || $scope.model.category_code == '') {
            alert('카테고리 코드를 입력하세요.');
            return;
        }
        if ($scope.model.item_no == null || $scope.model.item_no == '') {
            alert('지마켓 상품 코드를 입력하세요.');
            return;
        }
        if ($scope.model.item_name == null || $scope.model.item_name == '') {
            alert('지마켓 상품명을 입력하세요.');
            return;
        }
        if ($scope.model.gd_html == null || $scope.model.gd_html == '') {
            alert('상품 상세정보를 입력하세요.');
            return;
        }
        if ($scope.model.price == null || $scope.model.price == '') {
            alert('상품 가격을 입력하세요.');
            return;
        }
        if ($scope.model.auto_use_term_duration == null || $scope.model.auto_use_term_duration == '') {
            alert('쿠폰 유효기간을 입력하세요.');
            return;
        }
        if ($scope.model.apply_place == null || $scope.model.apply_place == '') {
            alert('사용처를 입력하세요.');
            return;
        }
        if ($scope.model.apply_place_url == null || $scope.model.apply_place_url == '') {
            alert('사용처 URL을 입력하세요');
            return;
        }
        if ($scope.model.stock_qty == null || $scope.model.stock_qty == '') {
            alert('재고 수량을 입력하세요.');
            return;
        }
        if ($scope.model.use_information == null || $scope.model.use_information == '') {
            alert('사용 유의사항을 입력하세요.');
            return;
        }
        if (typeof($scope.model.default_image) == 'undefined' || $scope.model.default_image == null) {
            alert('템플릿 이미지를 선택하세요');
            return;
        }

        usSpinnerService.spin('spinner-1');

        restFactory.request(baseURL).all('goods').post($scope.model).then(function(res) {
            console.log(res)
            if (res.errorCode == '00') {
                alert('등록 완료');
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

    $scope.onFilesSelected = function(files) {

        console.log($scope.model.default_image);

        if ($scope.model.item_no == null || $scope.model.item_no == '') {
            alert('지마켓 상품 코드를 입력해 주세요');
            return;
        }

        if ($scope.model.out_item_no == null || $scope.model.out_item_no == '') {
            alert('연동 코드를 입력해 주세요');
            return;
        }

        $scope.model.default_image = files[0];
        console.log($scope.model.default_image);

        var preview = document.querySelector('img');
        var reader  = new FileReader();

        if (typeof $scope.model.default_image != 'undefined') {
            reader.readAsDataURL($scope.model.default_image);

            Upload.upload({
                url: baseURL + '/template/upload',
                method: 'POST',
                data: {file: $scope.model.default_image,
                        'username': 'smartcon',
                        'item_no': $scope.model.item_no,
                        'out_item_no': $scope.model.out_item_no
                      }
            }).then(function(res) {
                console.log(res);
                preview.src = reader.result;
                console.log('Success ' + res.config.data.file.name + 'uploaded. Response: ' + res.data);
            }, function(res) {
                console.log(res);
                alert('업로드 실패 : ' + res.status);
                console.log('Error status: ' + res.status);
            }, function(evt) {
                var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
                console.log('progress: ' + progressPercentage + '% ' + evt.config.data.file.name);
            });

        } else {
            preview.src = "";
        }
    };

    $scope.onSearchEsmBrand = function() {
        usSpinnerService.spin('spinner-1');

        restFactory.request(baseURL).all('search_brands').get('', {'brand_name': $scope.model.brand_name}).then(function(res) {
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
})

.controller('ezwelXlsxRegistController', function($scope, usSpinnerService, restFactory) {
    console.log('ezwelXlsxRegistController');

    $scope.goods = [];
    $scope.filePath = null;
    $scope.logs = [];

    $scope.onGoodsAddForExcel = function(goods) {
        console.log('for excel');
        usSpinnerService.spin('spinner-1');

        var params = {
            cspCd: goods[0],
            cspGoodsCd: goods[1],
            goodsNm: goods[2],
            displayCd: goods[3],
            validPeriodExtYn: goods[4],
            exchangeSite: goods[5],
            concurrentCapa: goods[6],
            holidayCd: goods[7],
            contactNo: goods[8],
            openHm: goods[9],
            closeHm: goods[10],
            shopDispYn: goods[11],
            addr1: goods[12],
            addr2: goods[13],
            post: goods[14],
            parkingInfo: goods[15],
            resvYn: goods[16],
            resvCancelCd: goods[17],
            resvCancelEtc: goods[18],
            grpResvYn: goods[19],
            cancelYn: goods[20],
            normalPrice: goods[21],
            salePrice: goods[22],
            buyPrice: goods[23],
            buyQtyForEach: goods[24],
            goodsMemo: goods[25],
            goodsAddInfo: goods[26],
            notiCd: goods[27],
            sendPeriodExtYn: goods[28],
            imgUrl: goods[29],
            imgDetailUrl: goods[30],
            directions: goods[31],
            latitude: goods[32],
            longitude: goods[33],
            shopNm: goods[34],
            expireStartDd: goods[35],
            expireEndDd: goods[36],
            expireTypeCd: goods[37],
            afterIssExpireDay: goods[38],
            rnLength: goods[39],
            sendTypeCd: goods[40]
        };


        restFactory.request(baseURL).all('ezwelRegistGoods').post(params).then(function(res) {
            console.log(res);
            var result = {
                error_code: res.errorCode,
                error_message: res.errorMsg,
                goods_code: res.results.goods_code
            }

            $scope.logs.push(result);

            // if (res.errorCode == '00') {
            //     alert('등록 완료');
            // } else {
            //     alert('error code : ' + res.errorCode + ', error message : ' + res.errorMsg);
            //     $scope.logs.error_code = res.errorCode;
            //     $scope.logs.message = res.errorMsg;
            // }
        }, function(response) {
            alert('connection error');
        }).finally(function() {
            console.log('finally');
            usSpinnerService.stop('spinner-1');
        });
    };

    $scope.onDownExample = function() {
        console.log('down example');
        /* starting from this data */
        var obj = {
            'CSP 코드': '30000044',
            'CSP 상품코드(연동코드)': '5254',
            '상품명': '[스마트콘] 테스트상품',
            '웹/모바일 노출 구분코드': '00',
            '유효기간연장 가능여부': 'Y',
            '교환처': '교환처',
            '동시수용인원': '',
            '휴무일 코드': '01',
            '연락처': '02-561-0671',
            '영업시작시간': '0930',
            '영업종료시간': '1830',
            '매장정보 노출여부': 'Y',
            '주소1': '주소1',
            '주소2': '주소2',
            '우편번호': '01234',
            '주차안내': '',
            '당일예약 가능여부': '',
            '예약취소 코드': '04',
            '예약취소 기타': '',
            '단체예약 가능여부': '',
            '취소환불유무': '',
            '정상가': '10000',
            '판매가': '',
            '매입가(공급가)': '',
            '1인당 구매가능 수량 (1~1000)': '1',
            '상품 설명': '테스트 상품',
            '상품 추가정보': '상품 추가정보',
            '공정거래 고시정보': '1038',
            '기간만료 알림문자 발송': 'Y',
            '상품 이미지 URL (500 * 500)': 'http://www.giftsmartcon.com/shop/data/sum/bbq_31.png',
            '상품 상세 이미지 URL (900 * xxx)': 'http://www.giftsmartcon.com/bbq_detail.jpg',
            '오시는길': '포스코 사거리 xxxx',
            '위도': '37.499989',
            '경도': '127.033953',
            '매장명': '역삼점',
            '유효기간 시작일': '20180315125959',
            '유효기간 종료일': '20180515125959',
            '유효기간 타입(01: 기간선택, 02: 구매일로부터 n일)': '02',
            '발급일이후 유효기간': '90',
            '핀번호 자리수': '12',
            '발송타입(01: SMS, 02: LMS, 03: MMS)': '03'
        };
        var data = [];
        data.push(obj);

        /* generate a worksheet */
        var ws = XLSX.utils.json_to_sheet(data);

        /* add to workbook */
        var wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "Sheet1");

        /* write workbook (use type 'binary') */
        var wbout = XLSX.write(wb, {bookType:'xls', type:'binary'});

        saveAs(new Blob([s2ab(wbout)],{type:"application/octet-stream"}), "example.xls");
    };

    $scope.onGoodsRegist = function(index) {
        console.log(index);
        $scope.logs = [];

        if ($scope.goods.length > 0) {
            setTimeout(function() {
                console.log(index);

                $scope.onGoodsAddForExcel($scope.goods[index]);

                if ($scope.goods.length > ++index && typeof($scope.goods[index][0]) != 'undefined') {
                    $scope.onGoodsRegist(index);
                }

            }, 100);
        } else {
            alert('상품 리스트를 업로드 해주세요');
        }
    };

    $scope.$on('excelUpload', function(event, args) {
        $scope.$apply(function() {
            $scope.goods = args.goods;
            $scope.filePath = args.name;
        });
    });
})

.controller('goodsRegistXlsxController', function ($scope, $state, restFactory, usSpinnerService) {
    console.log('goodsRegistXlsxController');
    $scope.goods = [];
    $scope.filePath = null;
    $scope.model = {
        'radio': 'regist'
    };

    $scope.onGoodsAddForExcel = function(goods) {
        console.log('for excel');
        usSpinnerService.spin('spinner-1');

        var params = {
            expiration_date: goods[0],
            event_id: goods[1],
            out_item_no: goods[2],
            category_code: goods[3],
            item_name: goods[4],
            maker_no: goods[5],
            price: goods[6],
            gd_html: goods[7],
            help_desk_telno: goods[8],
            auto_term_duration: goods[9],
            auto_use_term_duration: goods[10],
            apply_place: goods[11],
            apply_place_url: goods[12],
            apply_place_telephone: goods[13],
            stock_qty: goods[14],
            use_information: goods[15],
            default_image: goods[16],
            find_guide: goods[17],
            publication_corp: goods[18],
            user_id: sessionStorage.getItem('userId')
        };

        restFactory.request(baseURL).all('goods').post(params).then(function(res) {
            console.log(res);
            if (res.errorCode == '00') {
                alert('등록 완료');
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

    $scope.onGoodsModifyForExcel = function(goods) {
        console.log('for excel');
        usSpinnerService.spin('spinner-1');

        var params = {
            expiration_date: goods[0],
            event_id: goods[1],
            out_item_no: goods[2],
            category_code: goods[3],
            item_name: goods[4],
            maker_no: goods[5],
            price: goods[6],
            gd_html: goods[7],
            help_desk_telno: goods[8],
            auto_term_duration: goods[9],
            auto_use_term_duration: goods[10],
            apply_place: goods[11],
            apply_place_url: goods[12],
            apply_place_telephone: goods[13],
            stock_qty: goods[14],
            use_information: goods[15],
            default_image: goods[16],
            find_guide: goods[17],
            publication_corp: goods[18],
            item_no: goods[19],
            user_id: sessionStorage.getItem('userId')
        };

        restFactory.request(baseURL).all('goods').post(params).then(function(res) {
            console.log(res);
            var result = {
                error_code: res.errorCode,
                error_message: res.errorMsg,
                goods_code: res.results.goods_code
            };

            $scope.logs.push(result);

        }, function(response) {
            alert('connection error');
        }).finally(function() {
            console.log('finally');
            usSpinnerService.stop('spinner-1');
        });
    };

    $scope.onGoodsRegist = function(index) {
        if ($scope.goods.length > 0) {
            setTimeout(function() {
                console.log(index);

                if ($scope.model.radio == 'regist') {
                    $scope.onGoodsAddForExcel($scope.goods[index]);
                } else {
                    $scope.onGoodsModifyForExcel($scope.goods[index]);
                }

                if ($scope.goods.length > ++index && typeof($scope.goods[index][0]) != 'undefined') {
                    $scope.onGoodsRegist(index);
                }

            }, 100);
        } else {
            alert('상품리스트를 업로드 해주세요');
        }
    };

    $scope.onDownExample = function() {
        console.log('down example');

        /* starting from this data */
        var obj = {
            '지마켓 상품 만료일': '20180226',
            '이벤트ID': '5254',
            '연동 코드': '0000026265',
            '카테고리 코드': '123455',
            '상품명': '테스트',
            '제조사번호': '201171998',
            '가격': '10000',
            '상품 상세 정보': '1234123',
            '고객센터': '02-561-0671',
            '쿠폰 정산기간': '7',
            '쿠폰 유효기간': '90',
            '사용처': '1234',
            '사용처 URL': 'http://test.com',
            '사용처 전화번호': '02-111-2222',
            '재고수량': '100',
            '사용 유의 사항': 'ㅇㅇㅇㅇㅇ',
            '상품 이미지': 'http://testimage.com',
            '찾아가는 길': 'test',
            '발행업체': '스마트콘'
        };
        var data = [];

        console.log($scope.model.radio);
        if ($scope.model.radio == 'modify') {
            obj['지마켓 상품코드'] = '12345';
        }

        data.push(obj);

        /* generate a worksheet */
        var ws = XLSX.utils.json_to_sheet(data);

        /* add to workbook */
        var wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "Sheet1");

        /* write workbook (use type 'binary') */
        var wbout = XLSX.write(wb, {bookType:'xls', type:'binary'});

        saveAs(new Blob([s2ab(wbout)],{type:"application/octet-stream"}), "example.xls");
    };

    $scope.$on('excelUpload', function(event, args) {
        $scope.$apply(function() {
            $scope.goods = args.goods;
            $scope.filePath = args.name;
        });
    });
})

.controller('goodsRegistAucController', function ($scope, $state, restFactory, usSpinnerService) {
    $scope.model = {
        event_id: null,
        goods_id: null,
        auc_item_no: null
    };

    $scope.onRegistGoods = function() {
        usSpinnerService.spin('spinner-1');

        restFactory.request(baseURL).all('goods_regist_auc').post($scope.model).then(function(res) {
            console.log(res)
            if (res.errorCode == '00') {
                // $scope.orderList = res.results;
                // $scope.figureOutOrdersToDisplay();

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

/**
 *File Input - custom call when the file has changed
 */
.directive('onFileChange', function() {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            var onChangeHandler = scope.$eval(attrs.onFileChange);

            element.bind('change', function() {
                scope.$apply(function() {
                    var files = element[0].files;
                    if (files) {
                        onChangeHandler(files);
                    }
                });
            });
        }
    };
});
