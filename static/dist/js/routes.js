angular
.module('app')
.config(['$stateProvider', '$urlRouterProvider', '$ocLazyLoadProvider', '$breadcrumbProvider', function($stateProvider, $urlRouterProvider, $ocLazyLoadProvider, $breadcrumbProvider) {

  $urlRouterProvider.otherwise('/login');

  $ocLazyLoadProvider.config({
    // Set to true if you want to see what and when is dynamically loaded
    debug: true
  });

  $breadcrumbProvider.setOptions({
    prefixStateName: 'app.main',
    includeAbstract: true,
    template: '<li class="breadcrumb-item" ng-repeat="step in steps" ng-class="{active: $last}" ng-switch="$last || !!step.abstract"><a ng-switch-when="false" href="{{step.ncyBreadcrumbLink}}">{{step.ncyBreadcrumbLabel}}</a><span ng-switch-when="true">{{step.ncyBreadcrumbLabel}}</span></li>'
  });

  $stateProvider
  .state('app', {
    abstract: true,
    templateUrl: '/static/dist/views/common/layouts/full.html',
    //page title goes here
    ncyBreadcrumb: {
      label: 'Root',
      skip: true
    },
    resolve: {
      loadCSS: ['$ocLazyLoad', function($ocLazyLoad) {
        // you can lazy load CSS files
        return $ocLazyLoad.load([{
          serie: true,
          name: 'Font Awesome',
          files: ['/static/dist/vendors/css/font-awesome.min.css']
        },{
          serie: true,
          name: 'Simple Line Icons',
          files: ['/static/dist/vendors/css/simple-line-icons.min.css']
        }]);
      }],
      loadPlugin: ['$ocLazyLoad', function ($ocLazyLoad) {
        // you can lazy load files for an existing module
        return $ocLazyLoad.load([{
          serie: true,
          name: 'chart.js',
          files: [
            '/static/dist/vendors/js/Chart.min.js',
            '/static/dist/vendors/js/angular-chart.min.js'
          ]
        }]);
      }],
    }
  })
  .state('app.main', {
    url: '/main',
    templateUrl: '/static/dist/views/main.html',
    //page title goes here
    ncyBreadcrumb: {
      label: 'Home',
    },
    //page subtitle goes here
    params: { subtitle: 'Welcome to ROOT powerfull Bootstrap & AngularJS UI Kit' },
    resolve: {
      loadPlugin: ['$ocLazyLoad', function ($ocLazyLoad) {
        // you can lazy load files for an existing module
        return $ocLazyLoad.load([
          {
            serie: true,
            name: 'chart.js',
            files: [
              '/static/dist/vendors/js/Chart.min.js',
              '/static/dist/vendors/js/angular-chart.min.js'
            ]
          },
        ]);
      }],
      loadMyCtrl: ['$ocLazyLoad', function($ocLazyLoad) {
        // you can lazy load controllers
        return $ocLazyLoad.load({
          files: ['/static/dist/js/controllers/main.js']
        });
      }]
    }
  })
  .state('appSimple', {
    abstract: true,
    templateUrl: '/static/dist/views/common/layouts/simple.html',
    resolve: {
      loadCSS: ['$ocLazyLoad', function($ocLazyLoad) {
        // you can lazy load CSS files
        return $ocLazyLoad.load([{
          serie: true,
          name: 'Font Awesome',
          files: ['/static/dist/vendors/css/font-awesome.min.css']
        },{
          serie: true,
          name: 'Simple Line Icons',
          files: ['/static/dist/vendors/css/simple-line-icons.min.css']
        }]);
      }],
    }
  })

  // Additional Pages
  .state('appSimple.login', {
    url: '/login',
    templateUrl: '/static/dist/views/pages/login.html',
    controller: 'loginController'
  })
  .state('appSimple.register', {
    url: '/register',
    templateUrl: '/static/dist/views/pages/register.html'
  })
  .state('appSimple.404', {
    url: '/404',
    templateUrl: '/static/dist/views/pages/404.html'
  })
  .state('appSimple.500', {
    url: '/500',
    templateUrl: '/static/dist/views/pages/500.html'
  })

  .state('app.cs', {
    url: "/cs",
    abstract: true,
    template: '<ui-view></ui-view>',
    ncyBreadcrumb: {
      label: 'CS'
    }
  })

  .state('app.cs.orderlist', {
    url: '/orderlist',
    templateUrl: '/static/dist/views/cs/order.html',
    controller: 'orderController',
    ncyBreadcrumb: {
      label: '주문내역 조회'
    }
  })

  .state('app.cs.resend', {
    url: '/resend',
    templateUrl: '/static/dist/views/cs/resend.html',
    controller: 'resendController',
    ncyBreadcrumb: {
      label: '재발송 처리'
    }
  })

  .state('app.blacklist', {
    url: '/blacklist',
    abstract: true,
    template: '<ui-view></ui-view>',
    ncyBreadcrumb: {
      label: '블랙리스트'
    }
  })

  .state('app.blacklist.search', {
    url: '/blacklist/search',
    templateUrl: '/static/dist/views/blacklist/blacklist-search.html',
    controller: 'blacklistSearchController',
    ncyBreadcrumb: {
      label: '블랙리스트 조회'
    }
  })

  .state('app.blacklist.regist', {
    url: '/blacklist/regist',
    templateUrl: '/static/dist/views/blacklist/blacklist-regist.html',
    controller: 'blacklistRegistController',
    ncyBreadcrumb: {
      label: '블랙리스트 등록'
    }
  })

  .state('app.goods', {
    url: '/goods',
    abstract: true,
    template: '<ui-view></ui-view>',
    ncyBreadcrumb: {
      label: '상품관리'
    }
  })

  .state('app.goods.goodslist', {
    url: '/goods/goodslist',
    templateUrl: '/static/dist/views/goods/goods-search.html',
    controller: 'goodsSearchController',
    ncyBreadcrumb: {
      label: '등록 상품 조회'
    }
  })

  .state('app.goods.regist', {
    url: '/goods/goodsregist',
    templateUrl: '/static/dist/views/goods/goods-regist.html',
    controller: 'goodsRegistController',
    ncyBreadcrumb: {
      label: '지마켓 상품 등록'
    }
  })

  .state('app.goods.xlsxRegist', {
    url: '/goods/xlsxRegist',
    templateUrl: '/static/dist/views/goods/goods-regist-xlsx.html',
    controller: 'goodsRegistXlsxController',
    ncyBreadcrumb: {
      label: '지마켓 상품 등록(엑셀)'
    }
  })

  .state('app.goods.ezwelXlsxRegist', {
    url: '/goods/ezwelXlsxRegist',
    templateUrl: '/static/dist/views/goods/ezwel-goods-regist-xlsx.html',
    controller: 'ezwelXlsxRegistController',
    ncyBreadcrumb: {
      label: '이지웰 상품 등록(엑셀)'
    }
  })

  .state('app.goods.regist_auc', {
    url: '/goods/regist_auc',
    templateUrl: '/static/dist/views/goods/goods-regist-auction.html',
    controller: 'goodsRegistAucController',
    ncyBreadcrumb: {
      label: '옥션 상품 등록'
    }
  })



}]);
