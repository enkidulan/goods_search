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
  'ui.slider',
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
.controller( 'SearchCtrl', function SearchController( $scope, $http, $rootScope ) {
  $scope.categories = [
    'All',
    'Apparel',
    'Appliances',
    'Automotive',
    'Baby',
    'Beauty',
    'Blended',
    'Books',
    'Classical',
    'DVD',
    'Electronics',
    'ForeignBooks',
    'GiftCards',
    'Grocery',
    'HealthPersonalCare',
    'Hobbies',
    'HomeImprovement',
    'Jewelry',
    'KindleStore',
    'Kitchen',
    'MP3Downloads',
    'MobileApps',
    'Music',
    'MusicTracks',
    'MusicalInstruments',
    'OfficeProducts',
    'PCHardware',
    'PetSupplies',
    'Shoes',
    'Software',
    'SportingGoods',
    'Toys',
    'VHS',
    'Video',
    'VideoDownload',
    'VideoGames',
    'Watches'
  ];

  $scope.isCollapsed = true;

  $scope.pagination = {
    current_page: 1,
    total_items: 1,
    max_size: 10,
    items_per_page: 5
  };
  $scope.displayed_results = [];
  $scope.pageChanged = function(){
    var start = ($scope.pagination.current_page - 1) * $scope.pagination.items_per_page;
    var end = start + $scope.pagination.items_per_page;
    $scope.displayed_results = $rootScope.search_results.slice(start, end);
  };

  $scope.avalivable_sorting = {
    // 'relevancerank': 'Best Match',
    // 'salesrank': 'Popular'
    'price': 'Price: Lowest first',
    '-price': 'Price: Highest first'
  };

  $scope.sort_by = 'relevancerank';
  $scope.set_sorting_by = function(field){
    $scope.sort_by = field;
    $scope.search();
  };

  $scope.category = 'All';
  $scope.keywords = '';
  $scope.set_category = function(category) {
    $scope.category = category;
    $scope.search();
    $scope.isCollapsed = true;
  };

  $scope.toggleDropdown = function($event) {
    $event.preventDefault();
    $event.stopPropagation();
    $scope.status.isopen = !$scope.status.isopen;
  };

  $scope.price_range = {
    MinimumPrice: 0,
    MaximumPrice: 1000
  };

  $scope.$watch('price_range.MinimumPrice', function(newValue, oldValue) {
   $scope.search();
  });
  $scope.$watch('price_range.MinimumPrice', function(newValue, oldValue) {
   $scope.search();
  });

  $scope.search_promice = null;
  $scope.pagination_promice = null;

  $scope.search = function(preview) {
    var params = '';
    params += '?Keywords=' + $scope.keywords;
    params += '&SearchIndex=' + $scope.category;
    params += '&MaximumPrice=' + $scope.price_range.MaximumPrice * 10;
    params += '&MinimumPrice=' + $scope.price_range.MinimumPrice * 10;
    params += '&Sort=' + $scope.sort_by;
    if ($scope.keywords) {
      $scope.search_promice = $http.get('/search' + params + '&preview=true').
          success(function(data, status, headers, config) {
            $rootScope.search_results = data;
            $scope.pagination.total_items = 100;
            $scope.pagination.current_page = 1;
            $scope.displayed_results = $rootScope.search_results.slice(0, $scope.pagination.items_per_page);
            $scope.pagination_promice = $http.get('/search' + params).
              success(function(data, status, headers, config) {
                $rootScope.search_results = data;
                $scope.pagination.total_items = $rootScope.search_results.length;
                // this callback will be called asynchronously
                // when the response is available
              });
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

