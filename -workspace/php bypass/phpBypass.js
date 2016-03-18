



var app = angular.module('phpBypassApp', [ 'ui.bootstrap', 'LocalStorageModule']);

app.controller('phpBypassCtrl', ['$scope', '$http', '$sce', '$rootScope', '$window', '$modal', 'localStorageService',
	function($scope, $http, $sce, $rootScope, $window, $modal, localStorageService){
		
		var testData = ['apple', 'banana', 'pineapple'];

		$scope.submitTestData = function(){
			$scope.callAPI(testData, "fruits", $scope.printFruits);
		}

		$scope.printFruits = function(){
			console.log($scope.fruits)
			
		}


		/******************************************************
		*	CODE BY ROB KOROBKIN
		*	- callAPI 
				- makes api call
				- saves response data in cookie
				- loads it in scope
				

			- init
				- gets list of keys in cookie
				- loads data into scope
		******************************************************/
	
		$scope.callAPI = function(request, varName, callback){
			var api_path = 'php_bypass.php';
			$http.post(api_path, request).then(
				function(response){

					var payLoad = response.data;

					// update list of keys in cookie
					var keys = localStorageService.get('keys');
					if(!keys) keys = [];
					if($.inArray(varName, keys) == -1){
						keys.push(varName);
					} 
					localStorageService.set('keys', keys);

					// save response data in cookie
					localStorageService.set(varName, payLoad);

					// load into scope
					$scope[varName] = payLoad;
				}
			);
		}

		$scope.init = function(){
			var keys = localStorageService.get('keys');
			if(keys){
				$.each(keys, function(index, key){
					$scope[key] = localStorageService.get(key);
				});
			}
		}

		$scope.init();
	}
]);

