# -*- coding: utf-8 -*-
"""Config parsing utilities
"""

from __future__ import absolute_import, print_function

import json
import os
import yaml

DEFAULTS = {"ENABLE_HTTP": True,
            "HTTP_PORT": 3000,
            "ENABLE_HTTPS": False,
            "HTTPS_PORT": 3001,
            "SERVER_KEY": "",
            "SERVER_CERT": "",
            "ZK_CONN_STRING": "127.0.0.1:2181",
            "ZK_ANNOUNCE_PATH": "/services/test-service/0.1/",
            "ZK_ANNOUNCE_HOST": "127.0.0.1",
            "ZK_CONN_TIMEOUT": 10000}

def parse_config_file(filename):
    """ Load configuration values from input file

    YAML and JSON are currently supported.

    Parameters:
    -----------
    filename: str
        Full path to the file containing the configuration.

    Returns:
    --------
    values: dict
        Loaded configuration values to use in the service.
    """

    ext = os.path.splitext(filename)[-1].lower()

    if ext in ['yml', 'yaml']:
        values = yaml.load(open(filename).read())
    elif ext == 'json':
        values = json.loads(open(filename).read())
    else:
        raise ValueError("Cannot parse extention type {}".format(ext))

    if set(values.keys()).issubset(DEFAULTS.keys()):
        raise ValueError("Provided config is not a subset of needed values.")

    return values


def cascade_config(config_file=None):
    """ Build complete config file considering ENV vars, files, and DEFAULTS

    Value precidence:
        1. Environment variables
        2. Values in specified configurationg file
        3. Defaults dictionary

    Parameters:
    -----------
    config_file: str,opt
        Full path to any desired configuration files.

    Returns:
    --------
    values: dict
        Configuration dictionary to be used in the service.
    """

    #-- start with default values
    values = DEFAULTS.copy()

    #-- update with config file values, if present
    if config_file:
        file_values = parse_config_file(config_file)
        values.update(file_values)

    #-- Environment variables take highest precidence
    for envvar in values.keys():
        if envvar in os.environ:
            new_val = os.environ[envvar]

            #-- integer
            if new_val.isdigit():
                new_val = int(new_val)

            values[envvar] = new_val

    return values
