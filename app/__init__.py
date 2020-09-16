# -*- coding:utf-8 -*-

import logging.config
from flask import Flask
from flask_restplus import Api

app = Flask(__name__, instance_relative_config=True)
api = Api(app)
app.config.from_pyfile('config.py')


root_logger = logging.getLogger('')
api_logger = logging.getLogger('api')
out_logger = logging.getLogger('out')
sql_logger = logging.getLogger('sql')


logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,  # this fixes the problem

    'formatters': {
        'standard': {
            'format': '%(asctime)s %(module)s[%(levelname)s] %(funcName)s@%(lineno)d: %(message)s'
        },
        'audit': {
            'format': '%(asctime)s||%(message)s'
        }
    },
    'handlers': {
        'default': {
            'level':'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'api': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filename': app.config['LOG_DIR']+'api.log'
        },
        'out': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filename': app.config['LOG_DIR']+'out.log'
        },
        'sql': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filename': app.config['LOG_DIR']+'sql.log'
        }
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },
        'api': {
            'handlers': ['api'],
            'level': 'INFO',
            'propagate': False
        },
        'out': {
            'handlers': ['out'],
            'level': 'INFO',
            'propagate': False
        },
        'sql': {
            'handlers': ['sql'],
            'level': 'INFO',
            'propagate': False
        },
        'sqlalchemy.engine': {
            'handlers': ['sql'],
            'level': 'ERROR',
            'propagate': False
        },
        'requests': {
            'handlers': ['out'],
            'level': 'WARNING',
            'propagate': False
        }
    }
})


from app.util import Util

celery = Util.make_celery(app)
from app.views.framework.base_view import baseProfile
app.register_blueprint(baseProfile, url_prefix='/')

from app.views.framework.error_define import exception
app.register_blueprint(exception, url_prefix='/error')

