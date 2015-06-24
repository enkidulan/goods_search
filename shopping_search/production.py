
from shopping_search.settings import *

FRONTEND_APP_PATH = os.path.join(PROJECT_ROOT, 'ngbp', 'bin')

ALLOWED_HOSTS = [ '*' ]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'shopping_services.log',
            'formatter': 'verbose'
        },
        'stream': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'shopping_search': {
            'handlers': ['file', 'stream'],
            'level': 'DEBUG',
        },
    }
}


