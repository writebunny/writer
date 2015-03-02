app.controller('DashboardCtrl', function ($scope, $resource, Book, Chapter) {

  $scope.display = function(mode, title) {
    for (key in $scope.dsp) {
      if ($scope.dsp.hasOwnProperty(key)) {
        $scope.dsp[key] = false;
      }
    }
    $scope.dsp[mode] = true;
    $scope.dsp.title = title;
  };

  $scope.addBook = function() {
    var book = new Book();
    book.$save(function () {
      $scope.books.push(book);
    });
  };

  $scope.addChapter = function() {
    var chapter = new Chapter({book: $scope.book.url});
    chapter.$save(function () {
      $scope.book.chapters.push(chapter);
    });
  };

  $scope.newBook = function() {
    $scope.book = new Book({title: ''});
    $scope.display('book', 'Add New Book');
  };

  $scope.editBook = function(item) {
    $scope.book = angular.copy(item);
    $scope.display('book', 'Edit Book');
  };

  $scope.openBook = function(book) {
    $scope.book = book;
    $scope.book.chapters = Chapter.query({book: book.id});
    $scope.display('contents');
  };

  $scope.openBookshelf = function() {
    $scope.display('bookshelf');
  };

  $scope.saveBook = function(item) {
    if (item.id) {
      item.$update(function() {
        var books = [];
        angular.forEach($scope.books, function(book) {
          if (book.id == item.id) {
            this.push(item);
          } else {
            this.push(book);
          }
        }, books);
        $scope.books = books;
        $scope.openBookshelf();
      });
    } else {
      item.$save(function() {
        $scope.books.push(item);
        $scope.openBookshelf();
      });
    }
  };

  // initialize
  $scope.dsp = {};
  $scope.books = Book.query(function() {
    $scope.openBookshelf();
  });
});
