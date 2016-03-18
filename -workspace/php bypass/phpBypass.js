



var app = angular.module('phpBypassApp', [ 'LocalStorageModule']);

app.controller('phpBypassCtrl', ['$scope', '$http', '$sce', '$rootScope', '$window', 'localStorageService',
	function($scope, $http, $sce, $rootScope, $window, localStorageService){
		
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
			var api_path = 'http://local.baxter-academy.org:5000/get_orders';

			var request = {
				token : 'maximillian.coury@baxter-academy.org',
				week_offset : 0
			}


			$http.post(api_path, request).then(
				function(response){

					console.log(response)

					// var payLoad = response.data;

					// // update list of keys in cookie
					// var keys = localStorageService.get('keys');
					// if(!keys) keys = [];
					// if($.inArray(varName, keys) == -1){
					// 	keys.push(varName);
					// } 
					// localStorageService.set('keys', keys);

					// // save response data in cookie
					// localStorageService.set(varName, payLoad);

					// // load into scope
					// $scope[varName] = payLoad;
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

