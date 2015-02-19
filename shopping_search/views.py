from django.http import HttpResponse, HttpResponseNotFound
from .settings import SERVICES_CONFIG, CATEGORIES
import json
from shopping_search.shopping_services.amazon import search as amazon_search
from shopping_search.shopping_services.yahoo import search as yahoo_search
import threading
import queue
import itertools


def searvise_search(request, service_name, service_search_func, result):
    params = {
        'keywords': request.GET.get('Keywords', ''),
        'maximum_price': request.GET.get('MaximumPrice'),
        'minimum_price': request.GET.get('MinimumPrice'),
        'sort': request.GET.get('Sort', None),
        'condition': request.GET.get('Condition', None),
        'is_preview': request.GET.get('preview', False),
        'category': CATEGORIES[
                request.GET.get('SearchIndex', 'All')][service_name]
    }
    result.put(service_search_func(**params))


def list_simple_merge(lists):
    return filter(None, itertools.chain(*itertools.zip_longest(*lists)))


def services_mearging_search(request, services):
    result = queue.Queue()
    threads = [
        threading.Thread(
            target=searvise_search,
            args=(request, name, func, result))
        for name, func in services.items()
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return tuple(list_simple_merge(result.queue))


def search(request):
    results = services_mearging_search(
        request,
        {'amazon': amazon_search,
         'yahoo': yahoo_search}
    )
    return HttpResponse(
        json.dumps(results), content_type="application/json")


def item(request):
    pass
    # if foo:
    #     return HttpResponseNotFound('<h1>Page not found</h1>')
    # else:
    return HttpResponse(
        json.dumps(response_data), content_type="application/json")
