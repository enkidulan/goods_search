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
import heapq
import codecs
from copy import copy
from operator import itemgetter, ge, le, lt, gt
import logging
LOGGER = logging.getLogger(__name__)


class DummyParamsCrypter(object):
    """
    Simple class for crypting services pages info
    """
    def __init__(self, keys):
        self.keys = keys

    def encrypt(self, dict_like_obj):
        """
        encrypt pages info
        """
        values = (str(dict_like_obj[k]) for k in self.keys)
        return ':'.join(values)

    def decrypt(self, value):
        """
        decrypt pages info
        """
        return {k: int(v) for k, v in zip(self.keys, value.split(':'))}


CRYPTER = DummyParamsCrypter(('amazon', 'yahoo', 'rakuten'))


def parse_request_params(request):
    """
    Parses request for required params and returns it.
    """
    params = {
        'keywords': request.GET.get('Keywords', ''),
        'maximum_price': request.GET.get('MaximumPrice', None),
        'minimum_price': request.GET.get('MinimumPrice', None),
        'sort': request.GET.get('Sort', None),
        'page': request.GET.get('page', 'null'),
        'category': request.GET.get('Category', None),
    }
    params['page'] = CRYPTER.decrypt(params['page']) \
        if params['page'] != 'null' \
        else {'amazon': 0, 'yahoo': 0, 'rakuten': 0}
    return params


def searvise_search(params, service_name, service_search_func, result):
    """ Wrapper for services search. Gets params from request and handle
    categories mapping for different services.
    """
    search_root = CATEGORIES[CATEGORIES['SearchRoot']]
    params['category'] = CATEGORIES.get(
        params['category'], search_root).get(service_name, None)
    params['page'] = params['page'][service_name]
    LOGGER.debug(
        'Looking on %s service, starting from page %s',
        service_name, params['page'])
    data = service_search_func(**params)
    LOGGER.debug('Found %s results on %s service', len(data), service_name)
    result.put({'service': service_name, 'data': data})


def merge_results(data, sort_key, pages):
    """
    Results merging function, merges results from different services into one
    list based on sorting params.
    """

    # CLEVER: make more appropriate and cheap dict making
    lists = dict()
    for i in data:
        if not i['data']:
            continue
        lists[i['service']] = i['data']

    if not sort_key:
        for service, results in lists.items():
            pages[service] += 1
        return pages, (j for i in itertools.zip_longest(*lists.values()) for j in i if j)
    reverse = False
    if sort_key.startswith('-'):
        reverse = True
        sort_key = sort_key[1:]
    for resultset in lists.values():
        resultset.sort(key=itemgetter(sort_key), reverse=reverse)

    index = -1 if reverse else 0
    edge_getter = max if reverse else max
    page_increase_comparator = ge if reverse else le
    break_comparator = lt if reverse else gt

    edge_value = edge_getter(
        map(itemgetter(sort_key), map(itemgetter(index), lists.values())))
    for service, results in lists.items():
        if page_increase_comparator(results[-1][sort_key], edge_value):
            pages[service] += 1
    results = []
    for result in heapq.merge(*lists.values(), key=itemgetter(sort_key), reverse=reverse):
        if break_comparator(result.get(sort_key), edge_value):
            break
        results.append(result)
    return pages, results


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

    page, results = merge_results(result.queue, params['sort'], params['page'])
    return page, tuple(results)


def search(request):
    """
    View that performs search
    """
    page, results = services_merging_search(
        request,
        {'amazon': amazon_search,
         'yahoo': yahoo_search,
         'rakuten': rakuten_search}
    )
    page = CRYPTER.encrypt(page)
    LOGGER.debug('Responding with %s results', len(results))
    data = {'page': page, 'results': results}
    data = json.dumps(data)
    data = codecs.encode(data)
    return HttpResponse(data, content_type="application/json")
