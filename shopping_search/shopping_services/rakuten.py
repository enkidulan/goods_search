from shopping_search.settings import SERVICES_CONFIG
import sys
import json
import codecs
from functools import wraps
from furl import furl
from uuid import uuid4
from itertools import chain


if sys.version_info.major == 2:
    from urllib2 import urlopen
else:
    from urllib.request import urlopen


def get_and_decode_json_by_url(url):
    """
    Fetches JSON data be making GET query and decodes JSON
    """
    req = urlopen(url)
    reader = codecs.getreader("utf-8")
    return json.load(reader(req))


def query_rakuten_api(function):
    """
    Decorator that handles API queries to rakuten. Its prepare environment
    for method call and handle response results for Yahoo service -
    dumps json and handle errors.
    """
    @wraps(function)
    def wrapper(self, **kwargs):
        # creating new instance of url request
        self.api_request = self._api_root.copy()
        # populating it with params and adding query path
        function(self, **kwargs)
        # adding applicationId to params
        self.api_request.args['applicationId'] = self.applicationId
        self.api_request.args['formatVersion'] = 2
        self.api_request.path.segments.append('Search')
        self.api_request.path.segments.append('20140222')
        self.api_request.path.normalize()
        return get_and_decode_json_by_url(self.api_request.url)
    return wrapper


class RakutenIchibaAPI(object):

    _api_root = furl(
        "https://app.rakuten.co.jp/services/api")

    def __init__(self, applicationid):
        self.applicationId = applicationid

    @query_rakuten_api
    def item_search(self, **kwargs):
        """
        Search Product, for supporter parameters take a look at
        https://webservice.rakuten.co.jp/api/ichibaitemsearch/
        """
        # adding url request prefix
        self.api_request.path.segments.append('IchibaItem')
        # TODO: add some params validation???
        self.api_request.args.update(**kwargs)

    @query_rakuten_api
    def genre_search(self, **kwargs):
        """
        Search genre, for supporter parameters take a look at
        http://webservice.rakuten.co.jp/api/ichibagenresearch/
        """
        # adding url request prefix
        self.api_request.path.segments.append('IchibaGenre')
        # TODO: add some params validation???
        self.api_request.args.update(**kwargs)


rakuten = RakutenIchibaAPI(**SERVICES_CONFIG['rakuten'])


def search(category, keywords, maximum_price,
           minimum_price, sort, condition, is_preview):
    params = dict(
        genreId=category,
        keyword=keywords
    )
    if maximum_price is not None:
        params['maxPrice'] = int(float(maximum_price))
    if minimum_price is not None:
        params['minPrice'] = int(float(minimum_price))
    if sort is not None:
        params['sort'] = '+itemPrice' if sort == 'price' else '-itemPrice'

    results = []
    for i in range(1 if is_preview else 10):
        result = rakuten.item_search(hits=30, page=i+1, **params)
        result = map(extract_data, result.get('Items', []))
        results.append(result)
    responce = tuple(filter(None, chain(*results)))
    return responce


def extract_data(product):
    data = {
        'service': 'rakuten',
        'price': product.get('itemPrice'),
        'image': product.get('mediumImageUrls', [])[0],
        'ASIN': product.get('itemCode') or str(uuid4()),
        # 'ProductId': product['itemCode'],
        'DetailPageURL': product.get('itemUrl'),
        'Label': product.get('itemCaption'),
        'EditorialReview': [
            {'name': 'Description',
             'value': product.get('itemCaption')}],
        'ProductGroup': product.get('genreId'),  # get it name to display
        'Title': product.get('itemName'),
        'Manufacturer': product.get('shopName'),
        'CustomerReviews': product.get('itemUrl'),  # XXX: no such thing
        'images': [
            {'SmallImage': small,
             'LargeImage': small.rsplit('?', 1)[0]}
            for small in product.get('smallImageUrls', [])],
        'ItemAttributes': [],
    }
    return data
