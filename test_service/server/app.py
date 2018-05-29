# -*- coding: utf-8 -*-
"""Create a lightweight Flask server to handle requests for the microservice.
"""

from __future__ import absolute_import, print_function

import os
import logging
import sys
logger = logging.getLogger("Test app")

from flask import Flask
from flask import jsonify, request
from flask import abort

from ..config.config import cascade_config



app = Flask(__name__.split('.')[0], static_folder='server/static')

print(__file__)
print(app.static_folder)

CONFIG = cascade_config()

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"Ping": "PONG"})


def setup_logging():
    # create the logging file handler
    logging.basicConfig(filename="test_service.log",
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)

    #-- handler for STDOUT
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logging.getLogger().addHandler(ch)

def launch_server():
    """ Main wrapper to launch the service

    This endpoint is exposed via entrypoints in the setup.py script.
    """

    setup_logging()

    CONFIG = cascade_config()
    logger.info("Config parsing complete")
    for key, val in CONFIG.items():
        logger.info("CONFIG: {}:{}".format(key, val))

    endpoints = {}
    if CONFIG['ENABLE_HTTP']:
        endpoints['http'] = CONFIG['HTTP_PORT']
    if CONFIG['ENABLE_HTTPS']:
        endpoints['https'] = CONFIG['HTTPS_PORT']


    if CONFIG['ENABLE_HTTPS']:
        #-- Ordering is important: cert,key tuple
        context = (CONFIG['SERVER_CERT'], CONFIG['SERVER_KEY'])
        app.run(host='0.0.0.0', port=CONFIG['HTTPS_PORT'], ssl_context=context)
    if CONFIG['ENABLE_HTTP']:
        app.run(host='0.0.0.0', port=CONFIG['HTTP_PORT'])