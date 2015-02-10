from django.http import HttpResponse, HttpResponseNotFound
from .settings import amazon_config
from amazon.api import AmazonAPI
import json


# locale = amazon_config.pop('locale')
# amazon = AmazonAPI(**amazon_config)
amazon = AmazonAPI('AKIAIHCK2H7WE2HKF2XQ', 'Qjnau2jA6HenJYM3JY0X46W693FtkDWFuJFp9sce',  '412112115052')


def search(request):
    # request.GET
    products = amazon.search(
        Keywords='\n'.join(request.GET['keywords']),
        SearchIndex='All')
    response_data = []
    for i, product in enumerate(products):
        if i == 20:
            break
        response_data.append({
            'title': product.title,
            'image': product.small_image_url,
            'price': product.price_and_currency[0],
            'currency': product.price_and_currency[1],
            'manufacturer': product.manufacturer,
            'publisher': product.publisher,
        })
    # if foo:
    #     return HttpResponseNotFound('<h1>Page not found</h1>')
    # else:
    return HttpResponse(
        json.dumps(response_data), content_type="application/json")
