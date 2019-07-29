// Default colors
var brandPrimary =  '#20a8d8';
var brandSuccess =  '#4dbd74';
var brandInfo =     '#63c2de';
var brandWarning =  '#f8cb00';
var brandDanger =   '#f86c6b';

var grayDark =      '#2a2c36';
var gray =          '#55595c';
var grayLight =     '#818a91';
var grayLighter =   '#d1d4d7';
var grayLightest =  '#f8f9fa';


// 테스트
//var baseURL = 'http://localhost:5556/smartconb2c/v1/b2c';

//상용
var baseURL = 'http://183.111.8.107:13081/smartconb2c/v1/b2c';

function appendZero(number) {
    if (number < 10) {
        return '0' + number;
    }
    return number;
};

/* generate a download */
function s2ab(s) {
    var buf = new ArrayBuffer(s.length);
    var view = new Uint8Array(buf);
    for (var i=0; i!=s.length; ++i) view[i] = s.charCodeAt(i) & 0xFF;
    return buf;
};

var sheet2arr = function(sheet) {
   var result = [];
   var row;
   var rowNum;
   var colNum;
   var range = XLSX.utils.decode_range(sheet['!ref']);
   for(rowNum = range.s.r; rowNum <= range.e.r; rowNum++){
      row = [];
       for(colNum=range.s.c; colNum<=range.e.c; colNum++){
          var nextCell = sheet[
             XLSX.utils.encode_cell({r: rowNum, c: colNum})
          ];
          if( typeof nextCell === 'undefined' ){
             row.push(void 0);
          } else row.push(nextCell.w);
       }
       result.push(row);
   }
   return result;
};

angular
.module('app', [
    'ui.router',
    'oc.lazyLoad',
    'ncy-angular-breadcrumb',
    'angular-loading-bar',
    'app.pagesController',
    'app.commonService',
    'app.orderController',
    'app.restService',
    'app.blacklistController',
    'app.goodsController',
    'app.repository',
    'angularSpinner',
    'ui.bootstrap',
    'ngFileUpload',
    'filereader'
])

.config(['cfpLoadingBarProvider', function(cfpLoadingBarProvider) {
  cfpLoadingBarProvider.includeSpinner = false;
  cfpLoadingBarProvider.latencyThreshold = 1;
}])

.config(['$qProvider', function ($qProvider) {
    $qProvider.errorOnUnhandledRejections(false);
}])

.run( function($rootScope, $stateParams, $trace, $transitions, $state) {
  // $rootScope.$on('$stateChangeSuccess',function(){
  //     document.body.scrollTop = document.documentElement.scrollTop = 0;
  //     console.log('state change success');
  // });

    // console.log($state);
    // console.log($stateParams);
    $rootScope.$state = $state;
    // $trace.enable('TRANSITION');

    console.log($state);
    $transitions.onStart({  }, function(trans) {
        console.log('trans start------');

        token = sessionStorage.getItem('token');

        console.log(token);

        if (token == null || token == '') {
            $state.go('appSimple.login');
        }
    });

    // $transitions.onError({  }, function(trans) {
    //     console.log('trans error ------');
    //     console.log(trans);
    //
    //     var auth = userFactory.getUserToken();
    //     console.log(auth);
    // });

    return $rootScope.$stateParams = $stateParams;
})
// 페이지 전환시 스피너


// .factory('userFactory', function() {
//     var userToken = null;
//
//     return {
//         setUserToken: function(token) {
//             userToken = token;
//         },
//         getUserToken: function() {
//             return userToken;
//         }
//     };
//
// });

.directive('importSheetJs', function($rootScope) {
    return {
      scope: { },
      link: function ($scope, $elm, $attrs) {
        $elm.on('change', function (changeEvent) {
            if (FileReader.prototype.readAsBinaryString === undefined) {
                FileReader.prototype.readAsBinaryString = function(fileData) {
                    var binary = "";
                    var pt = this;
                    var reader = new FileReader();
                    reader.onload = function (e) {
                        var bytes = new Uint8Array(reader.result);
                        var length = bytes.byteLength;
                        for (var i = 0; i < length; i++) {
                            binary += String.fromCharCode(bytes[i]);
                        }
                        //pt.result  - readonly so assign content to another property
                        pt.content = binary;
                        pt.onload(); // thanks to @Denis comment
                    }
                    reader.readAsArrayBuffer(fileData);
                }
            }

            var reader = new FileReader();

            console.log('read excel');

            reader.onload = function (e) {
                 /* read workbook */
                if (!e) {
                    var bstr = reader.content;
                } else {
                    var bstr = e.target.result;
                }

                console.log(bstr);

                var workbook = XLSX.read(bstr, {type:'binary'});

                console.log(workbook);
                var nameSheet = workbook.SheetNames[0];
                var sheetObj = workbook.Sheets[nameSheet];
                var sheetArray = sheet2arr(sheetObj);

                $rootScope.$broadcast('excelUpload', {'goods': sheetArray, 'name': changeEvent.target.files[0].name});
            };

            reader.readAsBinaryString(changeEvent.target.files[0]);

        });
      }
    };
});
