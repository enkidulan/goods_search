"""
Search handled for Yahoo Shopping service
"""
from yahoowebapi.shopping_web_service import YahooShoppingAPI
from shopping_search.settings import SERVICES_CONFIG

YAHOO = YahooShoppingAPI(**SERVICES_CONFIG['yahoo'])


# pylint: disable=too-many-arguments
def search(category, keywords, maximum_price,
           minimum_price, sort, page):
    """
    Performs Search. Returns 100 results per page.
    """
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

    hits = 100
    # pylint: disable=bad-builtin
    result = YAHOO.product_search(hits=hits, offset=page*hits, **params)
    results = map(extract_data, result['ResultSet']['0']['Result'].values())
    responce = tuple(filter(None, results))
    return responce


def extract_data(product):
    """
    Extracts data from search result item
    """
    if not isinstance(product, dict):
        return
    if not product.get('Code'):
        return
    data = {
        'service': 'yahoo',
        'price': " ".join([product.get('Price', {}).get('_attributes', {}).get('currency', None),
                           product.get('Price', {}).get('_value', None)]),
        'image': product.get('Image', {}).get('Medium'),
        'ASIN': product.get('Code'),
        # 'ProductId': product.get('ProductId'),
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
