angular.module( 'ngBoilerplate', [
  'templates-app',
  'templates-common',
  // 'ngBoilerplate.home',
  // 'ngBoilerplate.about',
  'ngBoilerplate.search',
  'ui.router',
  'ui.bootstrap',
  'cgBusy'
])

.config( function myAppConfig ( $stateProvider, $urlRouterProvider ) {
  $urlRouterProvider.otherwise( '/search' );
})

.run( function run () {
})

.controller( 'AppCtrl', function AppCtrl ( $scope, $location ) {
  $scope.search_results = [];

  $scope.$on('$stateChangeSuccess', function(event, toState, toParams, fromState, fromParams){
    if ( angular.isDefined( toState.data.pageTitle ) ) {
      $scope.pageTitle = toState.data.pageTitle + ' | ngBoilerplate' ;
    }
  });
})

;

