import logging
import logging.config
import logging.handlers
import pathlib
import timeit
import json
from io import StringIO
from datetime import datetime

class StringIOHandler(logging.StreamHandler):
    def __init__(self, stream=None):
        if stream is None:
            stream = StringIO()
        super().__init__(stream)
        self.stream = stream

def logger_init():
    global start_time, prev_time, step_counter, logger, config

    # Dynamically add the StringIOHandler to the logging.handlers module
    logging.handlers.StringIOHandler = StringIOHandler

    config_file = pathlib.Path('/app/src/logger_setup/config.json')
    with open(config_file) as f_in:
        config = json.load(f_in)

    logging.config.dictConfig(config)

    logger = logging.getLogger("my_logger")

    return logger