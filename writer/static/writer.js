var app = angular.module('app', ['ngMaterial', 'ngMessages', 'ngResource']);

app.config(['$interpolateProvider', function ($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
}]);

app.config(['$resourceProvider', function($resourceProvider) {
  // Don't strip trailing slashes from calculated URLs
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

app.controller('DashboardCtrl', function ($scope, $resource) {
  var Book = $resource('/api/books/:bookId', {bookId:'@id'});

  $scope.saveBook = function() {
    book.$save();
  };

  $scope.book = new Book({title: ''});
  $scope.books = Book.query();
});
