




var app = angular.module('tutorialApp', []);

app.controller('tutorialCtrl', ['$scope',
	function($scope){

		$scope.loadView = function(viewName){
			$scope.view = viewName;
		}
		
		$scope.loadView = function(viewAge){
			$scope.view = viewAge;
		}


		$scope.studentsList = ['Max','Simon', 'Ben'];

		$scope.studentOrder = ['Lo Mein','Burger','Hotdog']; 
		
		$scope.studentAge = ['Fifiteen','Sixteen','Seventeen'];

		$scope.studentsList = {
			0 : 'max',
			1 : 'simon', 
			2 : 'ben'
		};


		$scope.students = [
			{
				first_name : 'Max',
				last_name : 'Coury',
				age : 15,
				grade : 10,
				hobby: 'Soccer',
				order: 'Lo Mein',
			},

			{
				first_name : 'Ben',
				last_name : 'R-F',
				age : 17,
				grade : 12,
				hobby: 'Coding',
				order: 'Burger',
			}

		];

		// console.log($scope.studentsList);

		console.log($scope.studentAge);

		// console.log($scope.students);
		



	}
]);