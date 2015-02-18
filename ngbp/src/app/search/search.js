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
  })

  .state( 'search.item', {
    url: '?id',
    views: {
        "": {
          controller: 'SearchItemCtrl',
          templateUrl: 'search/item.tpl.html'
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
.controller( 'SearchCtrl', function SearchController( $scope, $http, $state, $rootScope, $timeout ) {
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
  };

  $scope.avalivable_sorting = {
    // 'relevancerank': 'Best Match',
    // 'salesrank': 'Popular'
    '': 'Default',
    'price': 'Price: Lowest first',
    '-price': 'Price: Highest first'
  };
  $scope.sort_by = '';
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
    MinimumPrice: 0,
    MaximumPrice: 1000
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

  $scope.search = function() {
    var params = '';
    params += '?Keywords=' + $scope.keywords;
    params += '&SearchIndex=' + $scope.category;
    params += '&MaximumPrice=' + $scope.price_range.MaximumPrice * 100;
    params += '&MinimumPrice=' + $scope.price_range.MinimumPrice * 100;
    params += ($scope.sort_by) ? '&Sort=' + $scope.sort_by : '';
    params += ($scope.condition) ? '&Condition=' + $scope.condition : '';

    if ($scope.keywords) {
      $state.go('search.results');
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

.controller( 'SearchResultsCtrl', function SearchResultsController( $scope, $http, $rootScope ) {

})

.controller( 'SearchItemCtrl', function SearchItemController( $scope, $stateParams, $rootScope, $sce) {
    $scope.trustSrc = function(src) {
      return $sce.trustAsResourceUrl(src);
    };
    $scope.trustHTML = function(html) {
      return $sce.trustAsHtml(html);
    };
    $scope.item = null;
    for (var i in $rootScope.search_results){
      if ($rootScope.search_results[i].ASIN == $stateParams.id){
        $scope.item = $rootScope.search_results[i];
        break;
      }
    }
    $scope.showed_image=$scope.item.images[0];
    $scope.change_image= function(index){
      $scope.showed_image=$scope.item.images[index];
    };
})

;

