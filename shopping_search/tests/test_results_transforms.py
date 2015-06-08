import unittest
from copy import deepcopy
from collections import OrderedDict
from testfixtures import compare, replace

from shopping_search.views import merge_results


TEST_SERVICES_DATA = (
    {'service': 'amazon', 'data': [{'price': 100}, {'price': 10}, {'price': 50}, {'price': 11}, {'price': 15}]},
    {'service': 'yahoo', 'data': [{'price': 100}, {'price': 80}, {'price': 95}]},
    {'service': 'rakuten', 'data': [{'price': 20}, {'price': 10}, {'price': 80}]},
    {'service': 'dummy', 'data': []},
)

class TestResultsMerging(unittest.TestCase):

    def setUp(self):
        self.data = deepcopy(TEST_SERVICES_DATA)
        self.pages = {'amazon': 0, 'yahoo': 0, 'rakuten': 0, 'dummy': 0}

    # def tearDown(self):
    #     pass

    @replace('builtins.dict', OrderedDict)
    def test_merge_relevance(self):
        next_pages, results = merge_results(
            self.data, None, self.pages)
        compare(results, [
            {'price': 100},
            {'price': 100},
            {'price': 20},
            {'price': 10},
            {'price': 80},
            {'price': 10},
            {'price': 50},
            {'price': 95},
            {'price': 80},
            {'price': 11},
            {'price': 15}]
        )
        compare(next_pages, {
            'amazon': 1, 'yahoo': 1, 'rakuten': 1, 'dummy': 0})

    def test_merge_from_highest_to_lowest(self):
        next_pages, results = merge_results(
            self.data, '-price', self.pages)
        compare(results, [
            {'price': 100},
            {'price': 100},
            {'price': 95},
            {'price': 80},
            {'price': 80}]
        )
        compare(next_pages, {
            'amazon': 0, 'yahoo': 1, 'rakuten': 0, 'dummy': 0})

    def test_merge_from_lowest_to_highest(self):
        next_pages, results = merge_results(
            self.data, 'price', self.pages)
        compare(results, [
            {'price': 10},
            {'price': 10},
            {'price': 11},
            {'price': 15},
            {'price': 20},
            {'price': 50},
            {'price': 80},
            {'price': 80}]
        )
        compare(next_pages, {
            'amazon': 0, 'yahoo': 0, 'rakuten': 1, 'dummy': 0})
