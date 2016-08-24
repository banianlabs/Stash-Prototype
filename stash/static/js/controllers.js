'use strict';

var stashApp = angular.module('Stash', []);

stashApp.controller('HeaderController', ['$scope',
function ($scope) {
	$scope.results = [
		{'name': 'cats', 'id': 1},
		{'name': 'dogs', 'id': 2},
		{'name': 'sunset', 'id': 3},
		{'name': 'waves', 'id': 4},
		{'name': 'branding', 'id': 5},
		{'name': 'fashion week', 'id': 6},
	];
	console.log("HeaderController scope: ", $scope);
}]);

stashApp.controller('IndexController', ['$scope', 'User',
function ($scope, User) {
	$scope.user = User.currentUser();
	console.log("IndexController scope: ", $scope);
}]);

stashApp.controller('AboutController', ['$scope', '$routeParams', 'User',
function ($scope, $routeParams, User) {
	var query = User.get({userId: $routeParams.id});

	console.log("AboutController scope: ", $scope);
}]);

stashApp.controller('UserStripController', ['$scope',
function ($scope) {

	// TODO Get user's posts. Dynamically load images here
	// TODO Initialize layout manager

	var params = {
		userId: $scope.user.id, 
		start: 0, // for dynamic loading
		end: 15
	};

	var query = Strip.get(params, function(images) {
		$scope.images = images.objects;
		console.log("UserStripController scope: ", $scope);
	});
}]);

stashApp.controller('StripController', ['$scope', 'Img',
function ($scope, Img) {
	// TODO get current collection of TagFilters as well
	var query = Img.get({userId: User.id}, function(images) {
		$scope.images = images.objects;
		console.log("StripController scope: ", $scope);
	});
}]);

stashApp.controller('StripImageController', ['$scope', '$routeParams', 'Img',
function ($scope, $routeParams, Img) {
	var query = Img.get({ imageId: $routeParams.imageId }, function(post) {
		$scope.post = post;
		console.log("StripImageController scope: ", $scope);
	});
}]);
