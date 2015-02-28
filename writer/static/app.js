var app = angular.module('app', ['ngCookies', 'ngMaterial', 'ngMessages', 'ngResource']);

app.run(['$http', '$cookies', function($http, $cookies) {
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.put['X-CSRFToken'] = $cookies.csrftoken;
}]);

app.config(['$interpolateProvider', function ($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
}]);

app.config(['$resourceProvider', function($resourceProvider) {
  // Don't strip trailing slashes from calculated URLs
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

app.factory('Book', ['$resource', function($resource) {
  return $resource('/api/books/:id/', {id:'@id'}, {
    'update': { method:'PUT' }
  });
}]);
