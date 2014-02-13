(function () {
    'use strict';

    
    var controllers = angular.module('expenseTracker.controllers');

    controllers
        .controller('ReportsController', [ '$scope', '$rootScope', 'Restangular',
            function ($scope, $rootScope, Restangular) {
                console.log("controller alive");
                

                $scope.dateOptions = {
                    //'year-format': "'yy'",
                    'starting-day': 1
                };            

                $scope.dataDomain = {};  

                $scope.disabledDate = function(date, mode){
                    var dt= moment(date);
                    if(!$scope.dataDomain.transaction_date_min || !$scope.dataDomain.transaction_date_max) return true;
                    return (dt.isBefore($scope.dataDomain.transaction_date_min) || dt.isAfter($scope.dataDomain.transaction_date_max))
                }


                $scope.interfaceState = {

                    startDate : null,
                    endDate : null,
                };
                


                $scope.resetInterface = function(){
                    $scope.interfaceState.startDate = $scope.dataDomain.transaction_date_min;
                    $scope.interfaceState.endDate = $scope.dataDomain.transaction_date_max;
                }



                var expenseDomain = Restangular.one('expense_domain', 1);

                expenseDomain.get({
                
                }).then(function(data){
                    console.log("domain", data);
                    $scope.dataDomain = data;
                    $scope.resetInterface();         
                    $scope.updateData();           
                    
                });


                $scope.updateData = function(){
                    var expenseDataByCat = Restangular.all('expense_by_category');
            
                    var params = {
                        start_date : moment($scope.interfaceState.startDate).format("YYYY-MM-DD"), 
                        end_date : moment($scope.interfaceState.endDate).format("YYYY-MM-DD") };
                    expenseDataByCat.getList(params).then(function(data){
                        $scope.expenseDataByCat = data;
                        var da = data;
                        $scope.testChart(da);
                    });


                    var expenseDataByCatAndMonth = Restangular.all('expense_by_category_and_month');
                    expenseDataByCatAndMonth.getList(params).then(function(data){
                        console.log("by category", data);
                        var categoriesData  = {}
                        for(var i=0,n=data.length;i<n;i++){
                            var datum = data[i];
                            var cat = datum.category;
                            categoriesData[cat] = categoriesData[cat] || [];
                            categoriesData[cat].push({ month:datum.month, amount:datum.amount, category:datum.category})
                        }

                        var series = [];
                        for(var x in categoriesData){
                            var serie = {key:x, values:_.sortBy(categoriesData[x], function(item){ return item.month })}
                            series.push(serie);
                        }
                        
                        $scope.testSecondChart(series);
                    });




                }



                $scope.expenses = [];

                
                var expenseData = Restangular.all('expense');
                expenseData.getList({
                
                }).then(function(data){
                    console.log("xxxx", data);
                    $scope.expenses = data;
                });


                


    


                $scope.testChart  = function(data){

                    nv.addGraph(function() {
                        var chart = nv.models.pieChart()
                            .x(function(d) { return d.category })
                            .y(function(d) { return d.amount })
                            .showLabels(true);
                      
                          d3.select("#chart svg")
                              .datum(data)
                            .transition().duration(1200)
                            .call(chart);

                        nv.utils.windowResize(chart.update);

                        return chart;
                    });


                };


                $scope.testSecondChart = function(data){
                    console.log(2, data)
                    nv.addGraph(function() {
                    var chart = nv.models.multiBarChart()
                        .x(function(d) { return d.month })
                        .y(function(d) { return d.amount })
                        //.margin({top: 30, right: 20, bottom: 50, left: 175})
                        
                        .tooltips(true)             //Show tooltips on hover.
                        //.transitionDuration(350)
                        //.showControls(true);        //Allow user to switch between "Grouped" and "Stacked" mode.
                 
                    chart.yAxis
                        .tickFormat(d3.format(',.2f'));

                    chart.xAxis
                        .tickFormat(function(d) { return d3.time.format('%b %d')(new Date(d)); })


                 
                    d3.select('#chart2 svg')
                        .datum(data)
                        .call(chart);
                 
                    nv.utils.windowResize(chart.update);
                 
                    return chart;
                  });
                }




                

        }]);



}());