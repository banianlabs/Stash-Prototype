'use strict';

angular.module('Stash', ['StashServices'])
	.config(['$routeProvider', '$locationProvider',
		function($routeProvider, $locationProvider) {
		$routeProvider
		.when('/', {
			templateUrl: 'static/partials/index.html',
			controller: 'Index11Controller'
		})
		.when('/a/:userId', {
			templateUrl: 'static/partials/about.html',
			controller: 'AboutController'
		})
		.when('/u/:userId', {
			templateUrl: 'static/partials/user-detail.html',
			controller: 'UserStripController'
		})
		.when('/s/', {
			templateUrl: 'static/partials/strip.html',
			controller: 'StripController'
		})
		.when('/p/:picId', {
			redirect: 'static/partials/strip-image.html',
			controller: 'StripImageController'
		})
		.otherwise({
			redirectTo: '/'
		});
		
		$locationProvider.html5Mode(true);
	}])
;