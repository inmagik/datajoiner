(function () {
    'use strict';
    angular.module('expenseTracker.controllers', []);
    var angularApp = angular.module("expenseTracker", ['expenseTracker.controllers', 'restangular', 'ui.bootstrap']);

    
    angularApp.config(['$httpProvider', function($httpProvider){
        //$httpProvider.defaults.useXDomain = true;
        //$httpProvider.defaults.withCredentials = true;
        //delete $httpProvider.defaults.headers.common['X-Requested-With'];
    }])

    .config(['RestangularProvider', function(RestangularProvider) {
        RestangularProvider.setBaseUrl("/api/v1");
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
    }]);


})();
