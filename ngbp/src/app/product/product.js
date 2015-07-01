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
angular.module( 'ngBoilerplate.product', [
  'ui.router',
  'plusOne'
])

/**
 * Each section or module of the site can also have its own routes. AngularJS
 * will handle ensuring they are all available at run-time, but splitting it
 * this way makes each module more "self-contained".
 */
.config(function config( $stateProvider ) {
  $stateProvider.state( 'product', {
    url: '/product/:productId',
    views: {
      "main": {
        controller: 'ProductCtrl',
        templateUrl: 'product/product.tpl.html'
      }
    },
    data:{ pageTitle: 'product' }
  });
})

/**
 * And of course we define a controller for our route.
 */
.controller( 'ProductCtrl', function ProductController( $scope, $stateParams, $rootScope, $sce, $state ) {
    console.log($state);

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

