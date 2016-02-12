




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
		
		$scope.order = function(){
			$scope.View = 'Order';
		}

		
	}
]);