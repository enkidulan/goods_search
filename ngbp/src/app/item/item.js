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
angular.module( 'ngBoilerplate.item', [
  'ui.router',
  'plusOne'
])

/**
 * Each section or module of the site can also have its own routes. AngularJS
 * will handle ensuring they are all available at run-time, but splitting it
 * this way makes each module more "self-contained".
 */
.config(function config( $stateProvider ) {
  $stateProvider.state( 'item', {
    url: '/item?id',
    views: {
      "main": {
        controller: 'ItemCtrl',
        templateUrl: 'item/item.tpl.html'
      }
    },
    data:{ pageTitle: 'item' }
  });
})

/**
 * And of course we define a controller for our route.
 */
.controller( 'ItemCtrl', function ItemController( $scope, $rootScope , $stateParams, $sce) {
    $scope.trustSrc = function(src) {
      return $sce.trustAsResourceUrl(src);
    };
    $scope.trustHTML = function(html) {
      return $sce.trustAsHtml(html);
    };
    // $scope.item = {"Title":"The Dalai Lama's Cat","price":"$8.57","ProductGroup":"Book","Label":"Hay House Visions","images":[{"LargeImage":"http://ecx.images-amazon.com/images/I/415g%2BFWNFLL.jpg","SmallImage":"http://ecx.images-amazon.com/images/I/415g%2BFWNFLL._SL75_.jpg"}],"EditorialReview":[{"name":"Product Description","value":"<div><p class=\"HHCover-BodyText\" style=\"margin: 0in 0in 0pt\"><I>“‘Oh! How adorable! I didn’t know you had a cat!’ she exclaimed.</I></p><p class=\"HHCover-BodyText\" style=\"margin: 0in 0in 0pt\"><I>I am always surprised how many people make this observation. Why should His Holiness <B>not</B> have a cat?</I></p><p class=\"HHCover-BodyText\" style=\"margin: 0in 0in 0pt\"><I>‘If only she could speak,’ continued the actress. ‘I’m sure she’d have such wisdom to share.’</I></p><p class=\"HHCover-BodyText\" style=\"margin: 0in 0in 0pt\"><I>And so the seed was planted . . . </I></p><p class=\"HHCover-BodyText\" style=\"margin: 0in 0in 0pt\"><I>I began to think that perhaps the time had come for me to write a book of my own—a book that would convey some of the wisdom I’ve learned sitting not at the feet of the Dalai Lama but even closer, on his lap. A book that would tell my own tale . . . how I was rescued from a fate too grisly to contemplate to become the constant companion of a man who is not only one of the world’s greatest spiritual leaders and a Nobel Peace Prize Laureate but also a dab hand with a can opener.”</I></p><p class=\"HHCover-BodyText\" style=\"margin: 0in 0in 0pt\"> </p><p class=\"HHCover-BodyText\" style=\"margin: 0in 0in 0pt\">Starving and pitiful, a mud-smeared kitten is rescued from the slums of New Delhi and transported to a life she could have never imagined. In a beautiful sanctuary overlooking the snow-capped Himalayas, she begins her new life as the Dalai Lama’s cat.</p><p class=\"HHCover-BodyText\" style=\"margin: 0in 0in 0pt\">Warmhearted, irreverent, and wise, this cat of many names opens a window to the inner sanctum of life in Dharamsala. A tiny spy observing the constant flow of private meetings between His Holiness and everyone from Hollywood celebrities to philanthropists to self-help authors, the Dalai Lama’s cat provides us with insights on how to find happiness and meaning in a busy, materialistic world. Her story will put a smile on the face of anyone who has been blessed by the kneading paws and bountiful purring of a cat.</p></div>"}],"ASIN":"1401940587","DetailPageURL":"http://www.amazon.com/The-Dalai-Lamas-David-Michie/dp/1401940587%3FSubscriptionId%3DAKIAIHCK2H7WE2HKF2XQ%26tag%3D412112115052%26linkCode%3Dxm2%26camp%3D2025%26creative%3D165953%26creativeASIN%3D1401940587","CustomerReviews":"http://www.amazon.com/reviews/iframe?akid=AKIAIHCK2H7WE2HKF2XQ&alinkCode=xm2&asin=1401940587&atag=412112115052&exp=2015-02-15T18%3A01%3A55Z&v=2&sig=KROMcCcmJ3vlnbrEQ7x9o4NaaPTZDzUsjWBVn2vuhd0%3D","ItemAttributes":[{"name":"ISBN","value":"1401940587"},{"name":"Author","value":"David Michie"},{"name":"ProductGroup","value":"Book"},{"name":"Label","value":"Hay House Visions"},{"name":"ProductTypeName","value":"ABIS_BOOK"},{"name":"PackageQuantity","value":"1"},{"name":"PartNumber","value":"9781401940584"},{"name":"EAN","value":"9781401940584"},{"name":"Title","value":"The Dalai Lama's Cat"},{"name":"ReleaseDate","value":"2012-10-01"},{"name":"Studio","value":"Hay House Visions"},{"name":"PublicationDate","value":"2012-10-01"},{"name":"Manufacturer","value":"Hay House Visions"},{"name":"NumberOfPages","value":"240"},{"name":"MPN","value":"9781401940584"},{"name":"Publisher","value":"Hay House Visions"},{"name":"Binding","value":"Paperback"},{"name":"NumberOfItems","value":"1"}],"image":"http://ecx.images-amazon.com/images/I/415g%2BFWNFLL._SL160_.jpg","Manufacturer":"Hay House Visions"};
    $scope.item = null;
    for (var i in $rootScope.search_results){
      if ($rootScope.search_results[i].ASIN == $stateParams.id){
        $scope.item = $rootScope.search_results[i];
        break;
      }
    }
    $scope.get_item_promice = null;
    $scope.get_item = function() {
      $scope.get_item_promice = $http.get('/item?service=amazon&id=').
          success(function(data, status, headers, config) {
            $scope.search_results = data;
            // this callback will be called asynchronously
            // when the response is available
          }).
          error(function(data, status, headers, config) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
          });

    };
})

;
