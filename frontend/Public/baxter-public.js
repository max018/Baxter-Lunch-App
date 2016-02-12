




var app = angular.module('baxterApp', []);

app.controller('baxterCtrl', ['$scope',
	function($scope){

		$scope.openOrderForm = function(){
			$scope.view = 'orderForm';
		}

		
	}
]);