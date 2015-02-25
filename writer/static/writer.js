var app = angular.module('app', ['ngMaterial', 'ngResource']);

app.config(['$interpolateProvider', function ($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
}]);

app.controller('DashboardCtrl', function ($scope, $resource) {
  var Book = $resource('/api/books/:bookId', {bookId:'@id'});

  $scope.books = Book.query();
});
