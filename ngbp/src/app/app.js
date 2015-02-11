angular.module( 'ngBoilerplate', [
  'templates-app',
  'templates-common',
  // 'ngBoilerplate.home',
  // 'ngBoilerplate.about',
  'ngBoilerplate.search',
  'ui.router',
  'ui.bootstrap'
])

.config( function myAppConfig ( $stateProvider, $urlRouterProvider ) {
  $urlRouterProvider.otherwise( '/search' );
})

.run( function run () {
})

.controller( 'AppCtrl', function AppCtrl ( $scope, $location ) {
  $scope.$on('$stateChangeSuccess', function(event, toState, toParams, fromState, fromParams){
    if ( angular.isDefined( toState.data.pageTitle ) ) {
      $scope.pageTitle = toState.data.pageTitle + ' | ngBoilerplate' ;
    }
  });
})

;

