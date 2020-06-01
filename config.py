import logging
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

LOGGING = {
    
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': f'{BASEDIR}/app.log',
        },
    },
    
    'loggers': {
        'NLP': {
            'handlers': ['file',],
            'level': logging.DEBUG,
        },
    },
}


class Configuration():
    DEBUG = True