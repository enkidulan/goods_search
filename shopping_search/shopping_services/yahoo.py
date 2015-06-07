"""
Search handled for Yahoo Shopping service
"""
from yahoowebapi.shopping_web_service import YahooShoppingAPI
from shopping_search.settings import SERVICES_CONFIG
from shopping_search.shopping_services.utils import IS_DATA_VALID
# import logging
# LOGGER = logging.getLogger(__name__)

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
        params['sort'] = '+price' if sort == 'price' else '-price'

    # we threat 100 results as 1 page which equals to 4 pages
    # on current API search request
    page = page * 4

    results = []
    # pylint: disable=bad-builtin
    for i in range(page, page + 4):
        responce = YAHOO.product_search(hits=25, offset=(page + i) * 25, **params)
        result_set = responce['ResultSet'].get('0', None)
        if not result_set:
            break
        items = result_set['Result'].values()
        for item in filter(IS_DATA_VALID, map(extract_data, items)):
            results.append(item)
    return results


def extract_data(product):
    """
    Extracts data from search result item
    """
    if not product or not isinstance(product, dict):
        return
    price = product.get('Price', {}).get('_value', None)
    data = {
        'service': 'yahoo',
        'currency': product.get(
            'Price', {}).get('_attributes', {}).get('currency', None),
        'price': price and int(price) or price,
        'image': product.get('Image', {}).get('Medium', None),
        'id': product.get('Code', None),
        # 'ProductId': product.get('ProductId', None),
        'DetailPageURL': product.get('Url', None),
        'Label': product.get('Description', None),
        'ProductGroup': product.get('Category', {}).get('Current', {}).get('Name', None),
        'Title': product.get('Name', None),
        'Manufacturer': product.get('Store', {}).get('Name', None),
        'images': [
            {'SmallImage': product.get('Image', {}).get('Small', None),
             'LargeImage': product.get('Image', {}).get('Medium', None)}],
        'CustomerReviews': product.get('Review', {}).get('Url', None),
        'ItemAttributes': [],
        'EditorialReview': [
            {'name': 'Description',
             'value': product.get('Description', None)}
        ],
    }
    return data
