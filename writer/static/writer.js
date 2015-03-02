app.controller('DashboardCtrl', function ($scope, $resource, Book, Chapter) {

  $scope.display = function(mode) {
    for (key in $scope.dsp) {
      if ($scope.dsp.hasOwnProperty(key)) {
        $scope.dsp[key] = false;
      }
    }
    $scope.dsp[mode] = true;
  };

  $scope.addBook = function() {
    var book = new Book();
    book.$save(function () {
      $scope.books.push(book);
    });
  };

  $scope.addChapter = function() {
    var chapter = new Chapter({book: $scope.book});
    chapter.$save(function () {
      $scope.book.chapters.push(chapter);
    });
  };

  $scope.openBook = function(book) {
    $scope.book = book;
    $scope.book.chapters = Chapter.query({book: book.id});
    delete $scope.chapter;
    delete $scope.scene;
    $scope.display('contents');
  };

  $scope.openBookshelf = function() {
    $scope.display('bookshelf');
  };

  $scope.openChapter = function(chapter) {
    console.log('test');
    $scope.chapter = chapter;
    // $scope.book.chapters = Chapter.query({book: book.id});
    delete $scope.scene;
    $scope.display('chapter');
  };

  // initialize
  $scope.dsp = {};
  $scope.books = Book.query(function() {
    $scope.openBookshelf();
  });
});
