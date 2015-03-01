var app = angular.module('app', ['ngCookies', 'ngMaterial', 'ngMessages', 'ngResource']);

/**
 * Insert the Django CSRF token into AJAX requests to API.
 */
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

app.factory('Chapter', ['$resource', function($resource) {
  return $resource('/api/chapters/:id/', {id:'@id'}, {
    'update': { method:'PUT' }
  });
}]);

/**
 * In place editing directive.
 * http://gaboesquivel.com/blog/2014/in-place-editing-with-contenteditable-and-angularjs/
 */
app.directive("contenteditable", function() {
  return {
    require: "ngModel",
    link: function(scope, element, attrs, ngModel) {

      function read() {
        var newValue = element.html().replace(/<br>/gi, '');
        if (newValue == ngModel.$viewValue || newValue == attrs['placeholder']) {
          return;
        }
        if (!newValue.trim().length && attrs.hasOwnProperty('required')) {
          element.html(ngModel.$viewValue);
          return;
        }
        ngModel.$setViewValue(newValue);
        var item = scope[attrs['wbItem']];
        item.$update();
      }

      ngModel.$render = function() {
        element.html(ngModel.$viewValue || attrs['placeholder'] || "");
      };

      element.bind("blur change", function() {
        scope.$apply(read);
      });
    }
  };
});
