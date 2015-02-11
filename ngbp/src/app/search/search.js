/**
 * Each section of the site has its own module. It probably also has
 * submodules, though this boilerplate is too simple to demonstrate it. Within
 * `src/app/home`, however, could exist several additional folders representing
 * additional modules that would then be listed as dependencies of this one.
 * For example, a `note` section could have the submodules `note.create`,
 * `note.delete`, `note.edit`, etc.
 *
 * Regardless, so long as dependencies are managed correctly, the build process
 * will automatically take take of the rest.
 *
 * The dependencies block here is also where component dependencies should be
 * specified, as shown below.
 */
angular.module( 'ngBoilerplate.search', [
  'ui.router',
  'plusOne'
])

/**
 * Each section or module of the site can also have its own routes. AngularJS
 * will handle ensuring they are all available at run-time, but splitting it
 * this way makes each module more "self-contained".
 */
.config(function config( $stateProvider ) {
  $stateProvider.state( 'search', {
    url: '/search',
    views: {
      "main": {
        controller: 'SearchCtrl',
        templateUrl: 'search/search.tpl.html'
      }
    },
    data:{ pageTitle: 'Search' }
  });
})


.directive('searchResultItem', function() {
  return {
    restrict: 'E',
    scope: {
      item: '=item'
    },
    templateUrl: 'search/search_result_item.tpl.html'
  };
})

/**
 * And of course we define a controller for our route.
 */
.controller( 'SearchCtrl', function SearchController( $scope, $http ) {
  $scope.categories = [
    'Lamps & Light Fixtures',
    'Amazon Instant Video',
    'Men',
    'Cycling',
    'Musical Instruments',
    'Shop Instant Video',
    'Kitchen & Dining',
    'Leisure Sports & Game Room',
    'Reload Your Amazon Balance',
    'Wine',
    'Desktops & Monitors',
    'For Baby',
    'Kindle Paperwhite',
    'Automotive Tools & Equipment',
    'Appstore for Android',
    'Appliances',
    'Audible Membership',
    'Team Sports',
    'Janitorial',
    'Subscribe & Save',
    'Amazon Elements',
    'Fire Tablets',
    'Sell Us Your Books',
    'Unlimited Photo Storage',
    'Printers & Ink',
    'Video Games',
    'Computer Parts & Components',
    'All Beauty'
  ];

  $scope.category = null;
  $scope.keywords = '';
  $scope.search_results = [];
  $scope.set_category = function(category) {
    $scope.category = category;
  };

  $scope.toggleDropdown = function($event) {
    $event.preventDefault();
    $event.stopPropagation();
    $scope.status.isopen = !$scope.status.isopen;
  };

  $scope.search = function() {
    if ($scope.keywords) {
      $http.get('/search?keywords=' + $scope.keywords).
          success(function(data, status, headers, config) {
            $scope.search_results = data;
            // this callback will be called asynchronously
            // when the response is available
          }).
          error(function(data, status, headers, config) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
          });
    }
  };

})

;

