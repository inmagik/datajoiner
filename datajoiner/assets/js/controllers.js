(function () {
    'use strict';

    
    var controllers = angular.module('angularApp.controllers');

    controllers
        .controller('JoinController', [ '$scope', '$rootScope', 'Restangular',
            function ($scope, $rootScope, Restangular) {


                $scope.left_hand = null;
                $scope.right_hand = null;

                $scope.$watch('left_hand', function(nv){
                    if(nv){
                        $scope.data.left_hand = nv.id;
                    }
                });

                $scope.$watch('right_hand', function(nv){
                    if(nv){
                        $scope.data.right_hand = nv.id;
                    }
                });

                $scope.annotations  =[];
                $scope.data = {
                    'left_hand' : null,
                    'right_hand' : null,
                    'left_hand_field' : null,
                    'right_hand_field' : null
                };


                var params = {};
                var userfileannotation = Restangular.all('userfileannotation');
                userfileannotation.getList(params).then(function(data){
                    $scope.annotations = data;
                    $scope.left_hand = $scope.annotations[0];
                    $scope.right_hand = $scope.annotations[1];
                    console.log($scope.data.right_hand)
                });

                $scope.saveTask = function(){
                    
                    var usertask = Restangular.all('usertask');
                    var promise;
                    if($scope.data.id){
                        promise = usertask.post($scope.data);
                    } else {
                        promise = usertask.post($scope.data)
                    }
                    promise.then(function(data){
                        $scope.data = data;
                        console.log("d", $scope.data)
                    })
                    
                }
                

            }
        ]);



}());