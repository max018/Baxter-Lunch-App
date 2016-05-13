

// CONFIG
var api_path = 'http://local.baxter-academy.org:8000/';
var CLIENT_ID = '609547274038-pe286rm7av3mopuklphse16kbd8c82ed.apps.googleusercontent.com';
window.onGAPILoad = function(){
	if('appScope' in window) {
		appScope.initGoogle();
	}
}


var app = angular.module('baxterApp', []);

app.controller('baxterCtrl', ['$scope', '$http',
	function($scope, $http){
		window.appScope = $scope; // create global pointer to app scope

		$scope.week_offset = 3;

		$scope.dayNames = [
			"monday", "tuesday", "wednesday", "thursday", "friday"
		];

		$scope.dates = [
			$scope.week_offset = "week in week_offset"
		];

		$scope.restaurants = [
			{
				"title" : "Portland Pie",
				"simple":false,
				"groups":{
					"pizza": [ 
						"Cheese",
						"Pepperoni",
						"Shipyard",
						"Great Diamond",
						"Noreaster"
					],
					"salad":[
						"Garden",
						"Caesar"
					]
				},
				"meals":{
					"2 Slices":{
						"pizza":2,
						"salad":0
					},
					"1 Slice, 1 Half Salad":{
						"pizza":1,
						"salad":1
					},
					"Full Salad":{
						"pizza":0,
						"salad":1
					}
				}
			},
			{
				"title" : "b.good",
				"simple":true,
				"options":[
					"Chicken Caesar Salad",
					"Southwestern Chicken Salad",
					"Avocado and Orange Salad",
					"Veggie Burger",
					"Chicken Sandwich",
					"Beef Burger",
					"Turkey Burger"
				]
			},
			{
				"title" : "Zen Chinese Bistro",
				"simple":true,
				"options":[
					"Chicken Lo Mein",
					"Pork Fried Rice"
				]
			},
			{
				"title" : "Kamasouptra",
				"simple":true,
				"options":[
					"Soup"
				]
			}
		]

	



	
	    $scope.orderListings = function(){
			$scope.View = 'Order Listings';
		}

		$scope.startOrder = function(day){
			$scope.newOrder = {
				"week_offset" : 3, 
			  	"day" : day, 
			  	"order" : {
					"restaurant": "",
					"option": "",
				}
			};
			$scope.View = 'ChooseRestaurant';
		}


		$scope.clickRestaurant = function(restaurant){
			$scope.current_restaurant = restaurant;
			$scope.newOrder.order.restaurant = restaurant.title;
			$scope.View = 'orderRecord';
		}

		
		$scope.submitOrder = function(){
			
			$scope.callAPI('place_order', $scope.newOrder, function(message){
				$scope.View = 'Confirmation';
			});
			
		}

		$scope.cancelOrder = function(dayIndex){

			var request = {
				week_offset : $scope.week_offset,
				day : dayIndex
			}

			var callback = function(response){
				$scope.days[dayIndex].order = null;
				$scope.View = 'Order Listings';
			}

			$scope.callAPI('cancel_order', request, callback) 	
		}



		$scope.View = 'Login';
		

		/* LOGIN STUFF */
		$scope.initGoogle = function(){
			gapi.load('auth2', function() {
				googleAuth = gapi.auth2.init({client_id: CLIENT_ID});
				googleAuth.then(function(){
					$scope.initApp();
				});
			});
		}

		$scope.initApp = function(){
			if (googleAuth.isSignedIn.get()) {
				$scope.access_token = googleAuth.currentUser.get().getAuthResponse().id_token;
				$scope.View = 'Loading';
				$scope.View = 'Order Listings';
				$scope.$digest();
				$scope.getOrders();
			}
			else {
				$scope.View = 'Login';
				$scope.$digest();
			}
		}

		$scope.signIn = function(){
			if(!googleAuth){
				$scope.initGoogle();
				return;
			}
			googleAuth.signIn().then(function(){
				$scope.initApp();
			});
		}

		$scope.signOut = function(){
			$scope.View = 'Login';
			googleAuth.signOut();
		}


		/* IF GOOGLE IS ALREADY UP BY THE TIME ANGULAR COMES ONLINE */
		if(googleAuth){
			$scope.initGoogle();	
		} 
		


		/* API STUFF */
		$scope.callAPI = function(endpoint, request, callback){
			request.token = $scope.access_token;
			$scope.View = 'Loading';
			$http.post(api_path + endpoint, request).then( 
				function(response){
					if(!response.data.success){
						console.log('something went wrong');
						console.log(response);	
						$scope.signOut();
					}
					callback(response.data);
				},
				function(response){
					console.log('something went wrong');
					console.log(response);
					$scope.signOut();
				}
			);
		}


		// GET ORDERS
		$scope.getOrders = function(week_offset){
			
			var request = {
				week_offset : $scope.week_offset 
			}

			var proccess_weekData = function(response){
				$scope.days = response.days;
				$scope.View = 'Order Listings';
			}

			$scope.callAPI('get_week', request, proccess_weekData);
		}





	}]);

