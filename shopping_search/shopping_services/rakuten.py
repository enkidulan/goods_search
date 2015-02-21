from shopping_search.settings import SERVICES_CONFIG
import sys
import json
import codecs
from functools import wraps
from furl import furl

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

    results = rakuten.item_search(
        genreId=category,
        keyword=keywords,
        maxPrice=maximum_price,
        minPrice=minimum_price,
        sort='+itemPrice' if sort == 'price' else '-itemPrice'
    )
    responce = map(extract_data, results['Items'])
    responce = tuple(filter(None, responce))
    return responce


def extract_data(product):
    try:
        data = {
            'service': 'rakuten',
            'price': product['itemPrice'],
            'image': product['mediumImageUrls'][0],
            'ASIN': product['itemCode'],
            # 'ProductId': product['itemCode'],
            'DetailPageURL': product['itemUrl'],
            'Label': product['itemCaption'],
            'EditorialReview': [
                {'name': 'Description',
                 'value': product['itemCaption']}],
            'ProductGroup': product['genreId'],  # get it name to display
            'Title': product['itemName'],
            'Manufacturer': product['shopName'],
            'CustomerReviews': product['itemUrl'],  # XXX: no such thing
            'images': [
                {'SmallImage': small,
                 'LargeImage': small.rsplit('?', 1)[0]}
                for small in product['smallImageUrls']],
            'ItemAttributes': [],
        }
    except Exception as exp:
        # XXX: !!!!
        return
    return data
