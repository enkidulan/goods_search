"""
Search handled for Amazon Shopping service
"""
import codecs
import hmac
import hashlib
import base64
from urllib.request import urlopen
from urllib.parse import quote
from time import strftime, gmtime
from lxml import etree
from shopping_search.settings import SERVICES_CONFIG
from shopping_search.shopping_services.utils import IS_DATA_VALID
from functools import wraps
from furl import furl

NSMAP = {
    'amazon': 'http://webservices.amazon.com/AWSECommerceService/2013-08-01'
}


class TextGetter(object):
    """
    Helper for getting nodes from amazon response
    """
    def __init__(self, item):
        self.item = item

    def __call__(self, *tags):
        path = './/amazon:' + '//amazon:'.join(tags)
        node = self.item.find(path, namespaces=NSMAP)
        return getattr(node, 'text', None)

    def allnodes(self, *tags):
        """
        returns all nodes
        """
        path = './/amazon:' + '//amazon:'.join(tags)
        return map(TextGetter, self.item.findall(path, namespaces=NSMAP))


def generate_signed_url(secret_key, qargs):
    """
    amazon URLs signer
    """
    keys = sorted(qargs.keys())
    args = '&'.join('%s=%s' % (
        key, quote(str(qargs[key]).encode('utf-8'), safe='~')) for key in keys)

    msg = 'GET'
    msg += '\necs.amazonaws.jp'
    msg += '\n/onca/xml'
    msg += '\n' + args

    signature = quote(
        base64.b64encode(
            hmac.new(secret_key.encode('utf-8'),
                     msg.encode('utf-8'), hashlib.sha256).digest()))
    return 'http://%s/onca/xml?%s&Signature=%s' % (
        'ecs.amazonaws.jp', args, signature)


def get_and_decode_json_by_url(url):
    """
    Fetches JSON data be making GET query and decodes JSON
    """
    req = urlopen(url)
    reader = codecs.getreader("utf-8")
    data = reader(req).read()
    # pylint: disable=no-member
    parser = etree.XMLParser()
    root = etree.XML(data, parser)
    items = []
    for item in TextGetter(root).allnodes('Item'):
        data = dict(
            service='amazon',
            price=item('LowestNewPrice', 'Amount'),
            currency=item('OfferSummary', 'LowestNewPrice', 'CurrencyCode'),
            image=item('MediumImage', 'URL'),
            id=item('ASIN'),
            DetailPageURL=item('DetailPageURL'),
            Label=item('ItemAttributes', 'Label'),
            ProductGroup=item('ItemAttributes', 'ProductGroup'),
            Title=item('ItemAttributes', 'Title'),
            Manufacturer=item('ItemAttributes', 'Manufacturer'),
            CustomerReviews=item('CustomerReviews', 'IFrameURL'),
            images=[{'SmallImage': img_set('SmallImage', 'URL'),
                     'LargeImage': img_set('LargeImage', 'URL')}
                    for img_set in item.allnodes('ImageSets', 'ImageSet')],
            ItemAttributes=[],
            EditorialReview=[
                {'value': i('Content'),
                 'name': i('Source')}
                for i in item.allnodes('EditorialReviews', 'EditorialReview')]
        )
        items.append(data)
    return items


def query_amazon_commerce_api(function):
    """
    Decorator that handles API queries to amazon. Its prepare environment
    for method call and handle response results for Yahoo service -
    dumps json and handle errors.
    """
    @wraps(function)
    def wrapper(self, **kwargs):
        """
        helper for creating new instance of url request
        """
        self.api_request = self.api_root.copy()
        self.api_request.args['AWSAccessKeyId'] = self.access_key
        self.api_request.args['AssociateTag'] = self.associate_tag
        self.api_request.args['Service'] = 'AWSECommerceService'
        self.api_request.args['Version'] = '2013-08-01'
        self.api_request.args['Timestamp'] = \
            strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
        # populating it with params and adding query path
        function(self, **kwargs)
        # adding additional to params
        url = generate_signed_url(self.secret_key, self.api_request.args)
        print(url)
        return get_and_decode_json_by_url(url)
    return wrapper


class API(object):
    """
    Simple Amazon API for searching items
    """
    api_root = furl(
        "http://webservices.amazon.com/onca/xml")
    api_request = None

    def __init__(self, access_key, secret_key, associate_tag, locale):
        self.access_key = access_key
        self.secret_key = secret_key
        self.associate_tag = associate_tag
        self.locale = locale

    @query_amazon_commerce_api
    def item_search(self, **kwargs):
        """
        Search Product, for supporter parameters take a look at
        http://docs.aws.amazon.com/AWSECommerceService/latest/DG/ItemSearch.html
        http://docs.aws.amazon.com/AWSECommerceService/latest/DG/rest-signature.html
        """
        # adding url request prefix
        self.api_request.args['Operation'] = 'ItemSearch'
        # IDEA: add some params validation???
        self.api_request.args.update(**kwargs)


AMAZON = API(**SERVICES_CONFIG['amazon'])


class SafeDetailsGetter(object):  # pylint: disable=too-few-public-methods
    """
    Helper to handle nasty amazon attribs getting
    """
    def __init__(self, product):
        self.product = product

    def __call__(self, attrs):
        attrs = attrs.split('.')
        current = self.product
        for attr in attrs:
            current = getattr(current, attr, None)
            if current is None:
                break
        return current


# pylint: disable=too-many-arguments
def search(category, keywords, maximum_price,
           minimum_price, sort, page):
    """
    Performs Search. Returns 10 results per page (amazon is kind slow)
    """
    # AWS limit API search only to 100 results, so we return all the results
    # with the 0 page
    if page > 0:
        return []
    params = dict(
        Keywords=keywords,
        ResponseGroup='ItemAttributes,OfferSummary,Images,Reviews,EditorialReview'
    )

    if maximum_price is not None:
        params['MaximumPrice'] = int(float(maximum_price)) * 100
    if minimum_price is not None:
        params['MinimumPrice'] = int(float(minimum_price)) * 100
    if sort is not None:
        params['Sort'] = sort

    params['SearchIndex'] = category['root']
    params['BrowseNode'] = category['node']
    # params['ItemPage'] = page + 1

    results = AMAZON.item_search(**params)

    response_data = []
    for page in range(1, 11):
        params['ItemPage'] = page
        for product in results:
            if not product['id']:
                continue
            product['price'] = product['price'] and int(product['price']) or product['price']
            if not IS_DATA_VALID(product):
                continue
            response_data.append(product)
    return response_data
