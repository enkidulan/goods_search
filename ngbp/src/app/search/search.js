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
  'ui.slider'
])

/**
 * Each section or module of the site can also have its own routes. AngularJS
 * will handle ensuring they are all available at run-time, but splitting it
 * this way makes each module more "self-contained".
 */
.config(function config( $stateProvider ) {
  $stateProvider.state( 'search', {
    abstract: true,
    url: '/search',
    views: {
      "main": {
        controller: 'SearchCtrl',
        templateUrl: 'search/search.tpl.html'
      }
    },
    data:{ pageTitle: 'Search' }
  })

  .state( 'search.results', {
    url: '',
    views: {
        "": {
          controller: 'SearchResultsCtrl',
          templateUrl: 'search/results.tpl.html'
        }
      }
  });

})


.directive('searchResultItem', function() {
  return {
    restrict: 'E',
    scope: {
      item: '=item'
    },
    templateUrl: 'search/search_result_row.tpl.html'
  };
})

/**
 * And of course we define a controller for our route.
 */
.controller( 'SearchCtrl', function SearchController( $scope, $http, $state, $rootScope, $timeout, $location, $anchorScroll) {
  $scope.categories = [
    'Baby',
    'DVD',
    'PetSupplies',
    'Grocery',
    'Electronics',
    'Toys',
    'HealthPersonalCare',
    'Appliances',
    'MusicTracks',
    'Automotive',
    'SportingGoods',
    'Music',
    'Hobbies',
    'Books',
    'MusicalInstruments',
    'Beauty',
    'Apparel',
    'Kitchen',
    'All',
    'PCHardware'
  ];

  $scope.isCollapsed = true;

  $scope.pagination = {
    current_page: 1,
    total_items: 1,
    max_size: 10,
    items_per_page: 10
  };
  $scope.displayed_results = [];
  $scope.pageChanged = function(){
    var start = ($scope.pagination.current_page - 1) * $scope.pagination.items_per_page;
    var end = start + $scope.pagination.items_per_page;
    $scope.displayed_results = $rootScope.search_results.slice(start, end);
    if (( $rootScope.search_results.length / $scope.pagination.items_per_page - $scope.pagination.current_page) < 2) {
      $scope.query_for_results(true);
    }
    // scrolling on results top
    $location.hash('searchForm');
    $anchorScroll();
  };

  $scope.avalivable_sorting = {
    // 'relevancerank': 'Best Match',
    // 'salesrank': 'Popular'
    '': 'Default',
    'price': 'Price: Lowest first',
    '-price': 'Price: Highest first'
  };
  $scope.sort_by = null;
  $scope.search_page = null;
  $scope.set_sorting_by = function(field){
    $scope.sort_by = field;
    $scope.search();
  };

  $scope.avalivable_conditions = {
    '': "New",
    Used: "Used",
    Collectible: "Collectible",
    Refurbished: "Refurbished",
    All : "All "
  };
  $scope.condition = '';
  $scope.set_condition = function(field){
    $scope.condition = field;
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
    MinimumPrice: null,
    MaximumPrice: null
  };

  var update_is_queued = false;
  var update_search = function(){
    $scope.search();
    update_is_queued = false;
  };
  $scope.$watch('price_range.MaximumPrice', function(newValue, oldValue) {
    if (!update_is_queued){
      update_is_queued = true;
      $timeout(update_search, 1000);
    }
  });
  $scope.$watch('price_range.MinimumPrice', function(newValue, oldValue) {
    if (!update_is_queued){
      update_is_queued = true;
      $timeout(update_search, 1000);
    }
  });

  $scope.search_promice = null;
  $scope.pagination_promice = null;

  $scope.search = function(extend) {
    $scope.search_promice = null;
    $scope.query_for_results(extend);
  };

  $scope.query_for_results = function(extend) {
    var params = '';
    params += '?Keywords=' + $scope.keywords;
    params += '&SearchIndex=' + $scope.category;
    params += ($scope.price_range.MaximumPrice) ? '&MaximumPrice=' + $scope.price_range.MaximumPrice : '';
    params += ($scope.price_range.MinimumPrice) ? '&MinimumPrice=' + $scope.price_range.MinimumPrice : '';
    params += ($scope.sort_by) ? '&Sort=' + $scope.sort_by : '';
    params += ($scope.condition) ? '&Condition=' + $scope.condition : '';
    params += '&page=' + $scope.search_page;

    if ($scope.keywords) {
      $state.go('search.results');
      var promice = $http.get('/search' + params);
      var isANewSearchRequest = typeof extend === 'undefined';
      if (isANewSearchRequest){
          $scope.search_promice = promice;
      } else {
          $scope.pagination_promice = promice;
      }
      promice.success(function(data, status, headers, config) {
            if (isANewSearchRequest){
                $scope.search_page = data.page;
                $rootScope.search_results = data.results;
                // $scope.pagination.current_page = 1;
                $scope.displayed_results = $rootScope.search_results.slice(0, $scope.pagination.items_per_page);
            } else {
                $scope.search_page = data.page;
                for (var i in data.results){
                    $rootScope.search_results.push(data.results[i]);
                }
            }
            $scope.pagination.total_items = $rootScope.search_results.length;
          }).
          error(function(data, status, headers, config) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
          });
    }
  };

})

.controller( 'SearchResultsCtrl', function SearchResultsController( $scope, $http, $rootScope ) {

})

;

