from django.http import HttpResponse, HttpResponseNotFound
from .settings import SERVICES_CONFIG, CATEGORIES
import json
from shopping_search.shopping_services.amazon import search as amazon_search


def search(request):
    results = amazon_search(request.GET)
    return HttpResponse(
        json.dumps(results), content_type="application/json")


def item(request):
    pass
    # if foo:
    #     return HttpResponseNotFound('<h1>Page not found</h1>')
    # else:
    return HttpResponse(
        json.dumps(response_data), content_type="application/json")
