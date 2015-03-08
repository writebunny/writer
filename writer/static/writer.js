app.controller('DashboardCtrl', function ($scope, $resource, Book, Chapter, File, Scene) {

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

  $scope.addChapter = function(book) {
    var chapter = new Chapter({book: book.url});
    chapter.$save(function () {
      book.chapters.push(chapter);
    });
  };

  $scope.addScene = function(chapter) {
    var scene = new Scene({chapter: chapter.url});
    scene.$save(function () {
      chapter.scenes.push(scene);
    });
  };

  $scope.openBook = function(book) {
    $scope.book = book;
    $scope.book.$touch();
    $scope.display('contents');
  };

  $scope.openBookshelf = function() {
    delete $scope.book;
    $scope.display('bookshelf');
  };

  $scope.openFiles = function(chapter) {
    $scope.chapter = chapter;
    if (!$scope.files) {
      $scope.files = File.query();
    }
    $scope.display('files');
  };

  $scope.linkFile = function(chapter, file) {
    var scene = new Scene({
        chapter: chapter.url,
        title: file.title,
        description: file.description,
        file_id: file.id,
        alternate_link: file.alternate_link,
        thumbnail_link: file.thumbnail_link
    });
    scene.$save(function () {
      chapter.scenes.push(scene);
      $scope.display('contents');
    });
  };

  // initialize
  $scope.dsp = {};
  $scope.books = Book.query(function() {
    for(var i=0, n=$scope.books.length; i < n; i++) {
      var book = $scope.books[i];
      if (book.is_active) {
        $scope.book = book;
        $scope.display('contents');
      }
      for(var j=0, n2=book.chapters.length; j < n2; j++) {
        var chapter = new Chapter(book.chapters[j]);
        book.chapters[j] = chapter;
        for(var k=0, n3=chapter.scenes.length; k < n3; k++) {
          chapter.scenes[k] = new Scene(chapter.scenes[k]);
        }
      }
    }
  });
  $scope.openBookshelf();
});
