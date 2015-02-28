app.controller('DashboardCtrl', function ($scope, $resource, Book) {

  $scope.display = function(mode, title) {
    for (key in $scope.dsp) {
      if ($scope.dsp.hasOwnProperty(key)) {
        $scope.dsp[key] = false;
      }
    }
    $scope.dsp[mode] = true;
    $scope.dsp.title = title;
  };

  $scope.newBook = function() {
    $scope.book = new Book({title: ''});
    $scope.display('book', 'Add New Book');
  };

  $scope.editBook = function(item) {
    $scope.book = angular.copy(item);
    $scope.display('book', 'Edit Book');
  };

  $scope.openBookshelf = function() {
    $scope.display('bookshelf');
  };

  $scope.save = function(item) {
    if (item.id) {
      item.$update();
    } else {
      item.$save();
    }
    if (item instanceof Book) {
      $scope.books = Book.query();
      $scope.openBookshelf();
    }
  };

  // initialize
  $scope.dsp = {};
  $scope.books = Book.query();
  $scope.openBookshelf();
});
