"""
Views for search.
"""
from django.http import HttpResponse
from .settings import CATEGORIES
import json
from shopping_search.shopping_services.amazon import search as amazon_search
from shopping_search.shopping_services.yahoo import search as yahoo_search
from shopping_search.shopping_services.rakuten import search as rakuten_search
import threading
import queue
import itertools
import codecs
from copy import copy


def parse_request_params(request):
    """
    Parses request for required params and returns it.
    """
    params = {
        'keywords': request.GET.get('Keywords', ''),
        'maximum_price': request.GET.get('MaximumPrice', None),
        'minimum_price': request.GET.get('MinimumPrice', None),
        'sort': request.GET.get('Sort', None),
        'page': request.GET.get('page', 0),
        'category': request.GET.get('Category', None),
    }
    return params


def searvise_search(params, service_name, service_search_func, result):
    """ Wrapper for services search. Gets params from request and handle
    categories mapping for different services.
    """
    search_root = CATEGORIES[CATEGORIES['SearchRoot']]
    params['category'] = CATEGORIES.get(
        params['category'], search_root).get(service_name, None)
    result.put(service_search_func(**params))


def list_simple_merge(lists, sort_key):
    """
    Results merging function, merges results from different services into one
    list based on sorting params.
    """
    results = [i for i in itertools.chain(*itertools.zip_longest(*lists)) if i]
    results.sort(key=sort_key)
    return results


def services_merging_search(request, services):
    """
    Preforms simultaneous non-blocking search for different shopping services
    and return search results merged into single list
    """
    result = queue.Queue()
    params = parse_request_params(request)
    threads = [
        threading.Thread(
            target=searvise_search,
            args=(copy(params), name, func, result))
        for name, func in services.items()
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return tuple(list_simple_merge(result.queue, params['sort']))


def search(request):
    """
    View that performs search
    """
    results = services_merging_search(
        request,
        {'amazon': amazon_search,
         'yahoo': yahoo_search,
         'rakuten': rakuten_search}
    )
    data = json.dumps(results)
    data = codecs.encode(data)
    return HttpResponse(data, content_type="application/json")
