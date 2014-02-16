(function () {
    'use strict';


var app = angular.module('angularApp.directives', []);


app.directive('helloWorld', function() {
  return {
    restrict: 'A',
    replace: true,
    template: '<p style="background-color:red">Hello World</p>',
    link: function(scope, elem, attrs) {

      
      
    }
  };
});


app.directive('taskBound', ['$timeout', function($timeout) {
  return {
    restrict: 'A',
    replace: false,
    scope: true,
    //template: '<p style="background-color:red">Hello World</p>',
    link: function(scope, elem, attrs) {

      scope.result = null;
      scope.firstRun = false;
      scope.data = {};
      scope.taskStateInternal = attrs.taskState;


      scope.updateDataLinked = function(){
        var expr = "[data-result-task-id="+scope.taskId+"]";
        console.log("xxx", expr)
        $(expr).text(JSON.stringify(scope.result));
      }
      

      scope.checkData = function(){
        scope.firstRun = true;
        
        $.ajax(
          {
            url : '/data/taskinfo/' + attrs.taskId.toString(),
            cache : false
          }
        ).success(function(data){
          console.log("hey", data);
          $timeout(function(){
            attrs.taskState = data.state;
            scope.taskStateInternal = data.state;
            scope.result = data.result;  
            scope.data = data;
          })
          scope.handler = null;

          if (!(data.state == 'SUCCESS' || data.state== 'FAILURE')){
            if(!scope.handler){
              scope.handler = setTimeout(scope.checkData , 2000);
            }
          } 
          //scope.updateDataLinked();

        });
      };
      
      //
      

      scope.$watch('taskStateInternal', function(newVal, oldVal){
          console.log("xxx", newVal, oldVal)
          if(!scope.firstRun){
            scope.checkData()
          }

          //$(elem).removeClass('task-state-'+oldVal);
          //$(elem).addClass('task-state-'+newVal);

      });

      
      
      
    }
  };
}]);


app.directive('userfileDetailPanel', function() {
  return {
    restrict: 'A',
    replace: true,
    templateUrl: getDjangoStaticPath('templates/user_file_panel.html'),
    link: function(scope, elem, attrs) {

      
      
    }
  };
});



}());