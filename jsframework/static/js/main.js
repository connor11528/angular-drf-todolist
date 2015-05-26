
var app = angular.module('drf-angular', [
	'ui.router'
]);

app.config(function($stateProvider, $urlRouterProvider){
	$stateProvider
		.state('home', {
			url: '/',
			templateUrl: '/static/templates/home.html',
			controller: 'MainCtrl'
		});

	$urlRouterProvider.otherwise('/');
});

app.controller('MainCtrl', function($scope){
	$scope.test = "I come from the angularz";
});