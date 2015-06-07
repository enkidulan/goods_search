"""
Search handled for Rakuten Shopping service
"""
from shopping_search.settings import SERVICES_CONFIG

from itertools import chain
from rakutenichiba import RakutenIchibaAPI
from shopping_search.shopping_services.utils import IS_DATA_VALID
# import logging
# LOGGER = logging.getLogger(__name__)


RAKUTEN = RakutenIchibaAPI(**SERVICES_CONFIG['rakuten'])


# pylint: disable=too-many-arguments
def search(category, keywords, maximum_price,
           minimum_price, sort, page):
    """
    Performs Search. Returns 100 results per page
    """
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

    # we threat 100 results as 1 page which equals to 4 pages
    # on current API search request
    page = page * 4

    # lets load 100 search results
    results = []
    # pylint: disable=bad-builtin
    for i in range(page, page + 4):
        result = RAKUTEN.item_search(hits=25, page=i+1, **params)
        result = map(extract_data, result.get('Items', []))
        results.append(result)
    responce = tuple(filter(IS_DATA_VALID, chain(*results)))
    return responce


def extract_data(product):
    """
    Extracts data from search result item
    """
    if not isinstance(product, dict) and product:
        return
    image = product.get('mediumImageUrls', None)
    price = product.get('itemPrice', None)
    data = {
        'service': 'rakuten',
        'currency': None,
        'price': price and int(price) or price,
        'image': image[0] if image else 0,
        'id': product.get('itemCode', None),
        # 'ProductId': product['itemCode', None],
        'DetailPageURL': product.get('itemUrl', None),
        'Label': product.get('itemCaption', None),
        'EditorialReview': [
            {'name': 'Description',
             'value': product.get('itemCaption', None)}],
        'ProductGroup': product.get('genreId', None),  # get it name to display
        'Title': product.get('itemName', None),
        'Manufacturer': product.get('shopName', None),
        'CustomerReviews': product.get('itemUrl', None),  # INFO: no such thing
        'images': [
            {'SmallImage': small,
             'LargeImage': small.rsplit('?', 1)[0]}
            for small in product.get('smallImageUrls', [])],
        'ItemAttributes': [],
    }
    return data
