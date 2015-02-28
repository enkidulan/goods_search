from yahoowebapi.shopping_web_service import YahooShoppingAPI
from shopping_search.settings import SERVICES_CONFIG
from uuid import uuid4
from itertools import chain

yahoo = YahooShoppingAPI(**SERVICES_CONFIG['yahoo'])


def search(category, keywords, maximum_price,
           minimum_price, sort, condition, is_preview):

    params = dict(
        category_id=category,
        query=keywords,
        )

    if maximum_price is not None:
        params['price_to'] = int(float(maximum_price))
    if minimum_price is not None:
        params['price_from'] = int(float(minimum_price))
    if sort is not None:
        params['sort'] = sort

    results = []
    for i in range(1 if is_preview else 10):
        result = yahoo.product_search(hits=50, offset=50*i, **params)
        result = map(extract_data, result['ResultSet']['0']['Result'].values())
        results.append(result)
    responce = tuple(filter(None, chain(*results)))
    return responce


def extract_data(product):
    if not isinstance(product, dict):
        return
    if product.get('ProductId') is None:
        return
    data = {
        'service': 'yahoo',
        'price': " ".join([product.get('Price', {}).get('_attributes', {}).get('currency', None),
                           product.get('Price', {}).get('_value', None)]),
        'image': product.get('Image', {}).get('Medium'),
        'ASIN': product.get('ProductId', str(uuid4())),
        'ProductId': product.get('ProductId'),
        'DetailPageURL': product.get('Url'),
        'Label': product.get('Description'),
        'ProductGroup': product.get('Category', {}).get('Current', {}).get('Name'),
        'Title': product.get('Name'),
        'Manufacturer': product.get('Store').get('Name'),
        'images': [
            {'SmallImage': product.get('Image').get('Small'),
             'LargeImage': product.get('Image').get('Medium')}],
        'CustomerReviews': product.get('Review').get('Url'),
        'ItemAttributes': [],
        'EditorialReview': [
            {'name': 'Description',
             'value': product.get('Description')}
        ],
    }
    return data
