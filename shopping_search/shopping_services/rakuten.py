"""
Search handled for Rakuten Shopping service
"""
from shopping_search.settings import SERVICES_CONFIG

from itertools import chain
from rakutenichiba import RakutenIchibaAPI


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

    # lets load 100 search results
    results = []
    # pylint: disable=bad-builtin
    for i in range(page, page + 4):
        result = RAKUTEN.item_search(hits=25, page=i+1, **params)
        result = map(extract_data, result.get('Items', []))
        results.append(result)
    responce = tuple(filter(None, chain(*results)))
    return responce


def extract_data(product):
    """
    Extracts data from search result item
    """
    if not product.get('itemCode'):
        return
    image = product.get('mediumImageUrls', None)
    data = {
        'service': 'rakuten',
        'price': product.get('itemPrice'),
        'image': image[0] if image else 0,
        'ASIN': product.get('itemCode'),
        # 'ProductId': product['itemCode'],
        'DetailPageURL': product.get('itemUrl'),
        'Label': product.get('itemCaption'),
        'EditorialReview': [
            {'name': 'Description',
             'value': product.get('itemCaption')}],
        'ProductGroup': product.get('genreId'),  # get it name to display
        'Title': product.get('itemName'),
        'Manufacturer': product.get('shopName'),
        'CustomerReviews': product.get('itemUrl'),  # INFO: no such thing
        'images': [
            {'SmallImage': small,
             'LargeImage': small.rsplit('?', 1)[0]}
            for small in product.get('smallImageUrls', [])],
        'ItemAttributes': [],
    }
    return data
