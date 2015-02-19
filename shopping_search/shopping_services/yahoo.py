from yahoowebapi.shopping_web_service import YahooShoppingAPI
from shopping_search.settings import SERVICES_CONFIG


yahoo = YahooShoppingAPI(**SERVICES_CONFIG['yahoo'])


def search(category, keywords, maximum_price,
           minimum_price, sort, condition, is_preview):

    results = yahoo.product_search(
        category_id=category,
        query=keywords,
        price_to=maximum_price,
        price_from=minimum_price,
        sort=sort,
    )
    responce = map(extract_data, results['ResultSet']['0']['Result'].values())
    responce = tuple(filter(None, responce))
    return responce


def extract_data(product):
    # import pdb; pdb.set_trace()
    try:
        if not product['ProductId']:  # XXX
            return
        data = {
            'service': 'yahoo',
            'price': " ".join([product['Price']['_attributes']['currency'],
                               product['Price']['_value']]),
            'image': product['Image']['Medium'],
            'ASIN': product['ProductId'],
            'ProductId': product['ProductId'],
            'DetailPageURL': product['Url'],
            'Label': product['Description'],
            'ProductGroup': product['Category']['Current']['Name'],
            'Title': product['Name'],
            'Manufacturer': product['Store']['Name'],
            'images': [
                {'SmallImage': product['Image']['Small'],
                 'LargeImage': product['Image']['Medium']}],
            # 'images': [
            #     {'SmallImage': i.SmallImage.URL.text,
            #      'LargeImage': i.LargeImage.URL.text}
            #     for i in product.ImageSets.ImageSet],
            'CustomerReviews': product['Review']['Url'],
            'ItemAttributes': [],
            # 'ItemAttributes': [
            #     {'name': k, 'value': v.text}
            #     for k, v in product.ItemAttributes.__dict__.items()
            #     if getattr(v, 'text', None) and k != 'Title'],
            'EditorialReview': [
                {'name': 'Description',
                 'value': product['Description']}
            ],
            # 'EditorialReview': [
            #     {'value': i.Content.text,
            #      'name': i.Source.text}
            #     for i in product.EditorialReviews.EditorialReview]
        }
    except Exception as exp:
        # XXX: !!!!
        return
    return data
