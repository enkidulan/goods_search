from django.http import HttpResponse, HttpResponseNotFound
from .settings import PROJECT_ROOT
import os.path
import json
from amazonproduct import API

amazon = API(cfg=os.path.join(PROJECT_ROOT, '.amazon.cfg'))


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


def search(request):
    amazon_request_params = dict(
        Keywords=request.GET.get('Keywords', ''),
        MaximumPrice=request.GET.get('MaximumPrice'),
        MinimumPrice=request.GET.get('MinimumPrice'),
        Sort=request.GET.get('Sort', None),
        Condition=request.GET.get('Condition', None),
        ResponseGroup='ItemAttributes,OfferSummary,Images,Reviews,EditorialReview')
    print amazon_request_params
    results = amazon.item_search(
        request.GET.get('SearchIndex', 'All'), **amazon_request_params)
    response_data = []
    for i, product in enumerate(results):
        data = extract_data(product)
        if data is None:
            continue
        response_data.append(data)
        if request.GET.get('preview', '') and i == 10:
            break
    return HttpResponse(
        json.dumps(response_data), content_type="application/json")


def item(request):
    pass
    # if foo:
    #     return HttpResponseNotFound('<h1>Page not found</h1>')
    # else:
    return HttpResponse(
        json.dumps(response_data), content_type="application/json")
