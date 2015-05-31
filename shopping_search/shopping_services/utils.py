"""
Utils for services searches
"""

DEFAUT_FIELDS = ('price', 'id')


class SearchValidator(object):  # pylint: disable=too-few-public-methods
    """
    Simple validator for parsed results
    """
    def __init__(self, reuquired_fields=None):
        self.reuquired_fields = reuquired_fields or DEFAUT_FIELDS

    def __call__(self, item):
        if not item:
            return False
        for field in DEFAUT_FIELDS:
            if not item.get(field, None):
                return False
        return True


IS_DATA_VALID = SearchValidator()
