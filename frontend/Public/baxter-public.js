




var app = angular.module('baxterApp', []);

app.controller('baxterCtrl', ['$scope',
	function($scope){

		$scope.View = 'Order Listings';
	
	    $scope.orderListings = function(){
			$scope.View = 'Order Listings';
		}
		
		$scope.submitOrder = function(){
			$scope.View = 'Confirmation';
		}

		$scope.restChoose = function(){
			$scope.View = 'Rest';
		}
		$scope.order = function(){
			$scope.View = 'Order';
		}
		$scope.orderZen = function(){
			$scope.View = 'OrderZen';
		}
		$scope.orderKama = function(){
			$scope.View = 'OrderKama';
			
		$scope.orderB = function(){
			$scope.View = 'OrderB';
		}
		}
	}
]);