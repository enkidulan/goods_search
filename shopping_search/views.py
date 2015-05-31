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
import operator
import logging
LOGGER = logging.getLogger(__name__)


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
    if not sort_key:
        return [i for i in itertools.chain(*itertools.zip_longest(*lists)) if i]
    results = [j for i in lists for j in i if j]
    # import pdb; pdb.set_trace()
    reverse = False
    if sort_key.startswith('-'):
        reverse = True
        sort_key = sort_key[1:]
    results.sort(key=operator.itemgetter(sort_key), reverse=reverse)
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
    LOGGER.debug('Responding with %s results', len(results))
    data = json.dumps(results)
    data = codecs.encode(data)
    return HttpResponse(data, content_type="application/json")
