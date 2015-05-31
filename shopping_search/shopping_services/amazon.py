"""
Search handled for Amazon Shopping service
"""
from amazonproduct import API
from shopping_search.settings import SERVICES_CONFIG
from shopping_search.shopping_services.utils import IS_DATA_VALID
import logging
LOGGER = logging.getLogger(__name__)


AMAZON = API(cfg=SERVICES_CONFIG['amazon'])


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


def extract_data(product):
    """
    Extracts data from search result item
    """
    pr_getter = SafeDetailsGetter(product)
    if not pr_getter('ASIN.text'):
        return
    price = pr_getter('OfferSummary.LowestNewPrice.Amount.text')
    data = {
        'service': 'amazon',
        'currency': pr_getter('OfferSummary.LowestNewPrice.CurrencyCode.text'),
        'price': price and int(price) or price,
        'image': pr_getter('MediumImage.URL.text'),
        'id': pr_getter('ASIN.text'),
        'DetailPageURL': pr_getter('DetailPageURL.text'),
        'Label': pr_getter('ItemAttributes.Label.text'),
        'ProductGroup': pr_getter('ItemAttributes.ProductGroup.text'),
        'Title': pr_getter('ItemAttributes.Title.text'),
        'Manufacturer': pr_getter('ItemAttributes.Manufacturer.text'),
        'images': [
            {'SmallImage': i.SmallImage.URL.text,
             'LargeImage': i.LargeImage.URL.text}
            for i in pr_getter('ImageSets.ImageSet') or []],
        'CustomerReviews': pr_getter('CustomerReviews.IFrameURL.text'),
        'ItemAttributes': [
            {'name': k, 'value': v.text}
            for k, v in product.ItemAttributes.__dict__.items()
            if getattr(v, 'text', None) and k != 'Title'],
        'EditorialReview': [
            {'value': i.Content.text,
             'name': i.Source.text}
            for i in pr_getter('EditorialReviews.EditorialReview') or []]
    }
    return data


# pylint: disable=too-many-arguments
def search(category, keywords, maximum_price,
           minimum_price, sort, page):
    """
    Performs Search. Returns 10 results per page (amazon is kind slow)
    """
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

    search_root = category['root']
    params['BrowseNode'] = category['node']
    params['ItemPage'] = page + 1

    results = AMAZON.item_search(search_root, **params)

    response_data = []
    for product in results:
        data = extract_data(product)
        if not IS_DATA_VALID(data):
            continue
        response_data.append(data)
        if len(response_data) >= 10:
            break
    LOGGER.debug('Found %s results', len(response_data))
    return response_data
