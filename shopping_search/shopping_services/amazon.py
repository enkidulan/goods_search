from amazonproduct import API
from shopping_search.settings import SERVICES_CONFIG
from uuid import uuid4


amazon = API(cfg=SERVICES_CONFIG['amazon'])


class SafeDetailsGetter(object):
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
    pr_getter = SafeDetailsGetter(product)
    if not pr_getter('ASIN.text'):
        return
    data = {
        'service': 'amazon',
        'price': pr_getter('OfferSummary.LowestNewPrice.FormattedPrice.text'),
        'image': pr_getter('MediumImage.URL.text'),
        'ASIN': pr_getter('ASIN.text'),
        'DetailPageURL': pr_getter('DetailPageURL.text'),
        'Label': pr_getter('ItemAttributes.Label.text'),
        'ProductGroup': pr_getter('ItemAttributes.ProductGroup.text'),
        'Title': pr_getter('ItemAttributes.Title.text'),
        'Manufacturer': pr_getter('ItemAttributes.Manufacturer.text'),
        'images': [
            {'SmallImage': i.SmallImage.URL.text,
             'LargeImage': i.LargeImage.URL.text}
            for i in pr_getter('ImageSets.ImageSet')],
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


def search(search_root, category, keywords, maximum_price,
           minimum_price, sort, condition, is_preview):
    params = dict(
        Keywords=keywords,
        ResponseGroup='ItemAttributes,OfferSummary,Images,Reviews,EditorialReview'
    )

    if maximum_price is not None:
        params['MaximumPrice'] = int(float(maximum_price)) * 100
    if minimum_price is not None:
        params['MinimumPrice'] = int(float(minimum_price)) * 100
    if condition is not None:
        params['Condition'] = condition
    if sort is not None:
        params['Sort'] = sort

    params['BrowseNode'] = category

    results = amazon.item_search(search_root, **params)

    response_data = []
    for i, product in enumerate(results):
        data = extract_data(product)
        if data is None:
            continue
        response_data.append(data)
        if is_preview and len(response_data) >= 6:
            break
        elif len(response_data) >= 20:
            break
    return response_data
