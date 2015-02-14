from django.http import HttpResponse, HttpResponseNotFound
from .settings import PROJECT_ROOT
import os.path
import json
from amazonproduct import API

amazon = API(cfg=os.path.join(PROJECT_ROOT, '.amazon.cfg'))


def search(request):
    results = amazon.item_search(
        request.GET.get('SearchIndex', 'All'),
        Keywords=request.GET.get('Keywords', ''),
        MaximumPrice=request.GET.get('MaximumPrice'),
        MinimumPrice=request.GET.get('MinimumPrice'),
        Sort=request.GET.get('Sort', None),
        ResponseGroup='Large')

    response_data = []
    # import pdb; pdb.set_trace()
    for i, product in enumerate(results):
        if request.GET.get('preview', '') and i == 5:
            break
        try:
            response_data.append({
                'price': product.OfferSummary.LowestNewPrice.FormattedPrice.text,
                'image': product.MediumImage.URL.text,
                'ASIN': product.ASIN.text,
                'DetailPageURL': product.DetailPageURL.text,
                'Label': product.ItemAttributes.Label.text,
                'ProductGroup': product.ItemAttributes.ProductGroup.text,
                'Title': product.ItemAttributes.Title.text,
                'Manufacturer': product.ItemAttributes.Manufacturer.text,
                'images': [
                    {'SmallImage': i.ImageSet.SmallImage.URL.text,
                     'LargeImage': i.ImageSet.LargeImage.URL.text}
                    for i in product.ImageSets],
                'CustomerReviews': product.CustomerReviews.IFrameURL.text,
                'ItemAttributes': [
                    {'name': k, 'value': v.text}
                    for k, v in product.ItemAttributes.__dict__.items()
                    if getattr(v, 'text', None) and k != 'Title'],
                'EditorialReview': [
                    {'value': i.EditorialReview.Content.text,
                     'name': i.EditorialReview.Source.text}
                    for i in product.EditorialReviews]

            })
        except:
            pass
    return HttpResponse(
        json.dumps(response_data), content_type="application/json")


def item(request):
    import pdb; pdb.set_trace()


    # if foo:
    #     return HttpResponseNotFound('<h1>Page not found</h1>')
    # else:
    return HttpResponse(
        json.dumps(response_data), content_type="application/json")
