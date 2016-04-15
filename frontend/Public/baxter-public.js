
var app = angular.module('baxterApp', []);

app.controller('baxterCtrl', ['$scope',
	function($scope){

		$scope.dayNames = [
			"monday", "tuesday", "wednesday", "thursday", "friday"
		];

		$scope.restaurants = [
			{
				title : "Portland Pie",
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

		console.log($scope.restaurants)


		$scope.days = [
			{	"holiday": null, 
				"order": {
					"restaurant": "Zen Chinese Bistro",
					"option": "Pork Fried Rice"
				}
			},

			{	"holiday": "New Year's Eve", 
				"order": null
			},

			{	"holiday": "New Year's Day", 
				"order": null
			},

			{	"holiday": null, 
				"order": {
					"restaurant": "Portland Pie",
					"option": "Pizza: Cheese, Cheese"
				}
			},	 

			{	"holiday": null, 
				"order": null
			},	
		];



		$scope.View = 'Order';
	
	    $scope.orderListings = function(){
			$scope.View = 'Order Listings';
		}

		$scope.startOrder = function(day){
			console.log(day)
			$scope.View = 'ChooseRestaurant';
		}
		
		$scope.submitOrder = function(){
			$scope.View = 'Confirmation';
		}

		
		
		$scope.order = function(){
			$scope.View = 'Order';
		}
		
		$scope.orderZen = function(){
			$scope.View = 'OrderZen';
		}
		
		$scope.orderKama = function(){
			$scope.View = 'OrderKama';
		}
		
		$scope.orderB = function(){
			$scope.View = 'OrderB';
		}
	}
]);