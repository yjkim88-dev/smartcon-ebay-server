angular.module('app.restService', ['restangular'])

.config(['$httpProvider', function($httpProvider) {
    $httpProvider.interceptors.push('httpInterceptor');
}])


.factory('httpInterceptor', function($q) {
    return {
        request : request,
        responseError: responseError
    }

    function request(config) {
        // config.headers['SMARTBAG-API-KEY'] = '521dd0360dce42b6b2a594a0744e93bd65709a493ff3826c';
        console.log(sessionStorage.getItem('token'));
        if (sessionStorage.getItem('token') != null) {
            config.headers['restKey'] = sessionStorage.getItem('userId') + ',' + sessionStorage.getItem('token');

            console.log(config.headers['restKey']);
        }

        return config;
    }

    function responseError(response) {
        console.log(JSON.stringify(response));
        if (response.status == 401) {
            if (response.data) {

            }
        }

        return $q.reject(response);
    }
})

// .config(function(RestangularProvider) {
//     console.log(sessionStorage.getItem('userId'));
//     console.log(sessionStorage.getItem('token'));
//
//     RestangularProvider.setDefaultHeaders({'restKey': sessionStorage.getItem('userId') + ','  + sessionStorage.getItem('token')});
//     // RestangularProvider.setDefaultHeaders({'restKey': 'sadasdasd'});
// })

.factory('restFactory', function(Restangular) {
    return {
        request: function(baseUrl) {
            return Restangular.withConfig(function(RestangularConfigurer) {
                RestangularConfigurer.setBaseUrl(baseUrl);
            });
        }
    };

});
