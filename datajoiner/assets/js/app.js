(function () {
    'use strict';
    angular.module('angularApp.controllers', []);
    angular.module('angularApp.directives', []);

    var angularApp = angular.module("angularApp", ['angularApp.controllers', 'angularApp.directives', 
        'restangular', 'ui.bootstrap']);

    
    angularApp.config(['$httpProvider', function($httpProvider){
        //$httpProvider.defaults.useXDomain = true;
        //$httpProvider.defaults.withCredentials = true;
        //delete $httpProvider.defaults.headers.common['X-Requested-With'];
    }])

    .config(function($interpolateProvider) {
        //$interpolateProvider.startSymbol('[{[');
         //$interpolateProvider.endSymbol(']}]');
    })

    .config(['RestangularProvider', function(RestangularProvider) {
        RestangularProvider.setBaseUrl("/data/api");
        RestangularProvider.setResponseExtractor(function(response, operation, what, url) {
            var newResponse;
            if (operation === "getList") {
                newResponse = response.objects;
                newResponse.metadata = response.meta;
            } else {
                newResponse = response;
            }
            return newResponse;
        });
        RestangularProvider.setRequestSuffix('/?');
    }])


    


})();
