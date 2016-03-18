




var app = angular.module('tutorialApp', []);

app.controller('tutorialCtrl', ['$scope',
	function($scope){

		$scope.loadView = function(viewName){
			$scope.view = viewName;
		}
		

		$scope.studentsList = ['max','simon', 'ben'];

		$scope.studentsList = {
			0 : 'max',
			1 : 'simon', 
			2 : 'ben'
		};


		$scope.students = [
			{
				first_name : 'max',
				last_name : 'coury',
				grade : 10,
				hobby: 'soccer'
			},

			{
				first_name : 'ben',
				last_name : 'r-f',
				grade : 12,
				hobby: 'coding'
			}

		];

		// console.log($scope.studentsList);


		// console.log($scope.students);
		



	}
]);