from amazonproduct import API
from shopping_search.settings import SERVICES_CONFIG


amazon = API(cfg=SERVICES_CONFIG['amazon'])


def extract_data(product):
    try:
        data = {
            'price': product.OfferSummary.LowestNewPrice.FormattedPrice.text,
            'image': product.MediumImage.URL.text,
            'ASIN': product.ASIN.text,
            'DetailPageURL': product.DetailPageURL.text,
            'Label': product.ItemAttributes.Label.text,
            'ProductGroup': product.ItemAttributes.ProductGroup.text,
            'Title': product.ItemAttributes.Title.text,
            'Manufacturer': product.ItemAttributes.Manufacturer.text,
            'images': [
                {'SmallImage': i.SmallImage.URL.text,
                 'LargeImage': i.LargeImage.URL.text}
                for i in product.ImageSets.ImageSet],
            'CustomerReviews': product.CustomerReviews.IFrameURL.text,
            'ItemAttributes': [
                {'name': k, 'value': v.text}
                for k, v in product.ItemAttributes.__dict__.items()
                if getattr(v, 'text', None) and k != 'Title'],
            'EditorialReview': [
                {'value': i.Content.text,
                 'name': i.Source.text}
                for i in product.EditorialReviews.EditorialReview]
        }
    except:
        # XXX: !!!!
        return
    return data


def search(search_params):
    amazon_request_params = dict(
        Keywords=search_params.get('Keywords', ''),
        MaximumPrice=search_params.get('MaximumPrice'),
        MinimumPrice=search_params.get('MinimumPrice'),
        Sort=search_params.get('Sort', None),
        Condition=search_params.get('Condition', None),
        ResponseGroup='ItemAttributes,OfferSummary,Images,Reviews,EditorialReview')
    results = amazon.item_search(
        search_params.get('SearchIndex', 'All'), **amazon_request_params)
    response_data = []
    for i, product in enumerate(results):
        data = extract_data(product)
        if data is None:
            continue
        response_data.append(data)
        if search_params.get('preview', '') and len(response_data) >= 10:
            break
    return response_data
