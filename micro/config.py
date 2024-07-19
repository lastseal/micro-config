# -*- coding: utf-8 -*

from datetime import datetime

import logging
import dotenv
import signal
import sys
import os

dotenv_path = os.path.join(os.getcwd(), ".env")
dotenv.load_dotenv( dotenv_path )

LOG_LEVEL = os.getenv("LOG_LEVEL") or 'INFO'

if LOG_LEVEL.lower() == "debug":
    logging.basicConfig(
        format='%(asctime)s.%(msecs).03d [%(pathname)s:%(lineno)d] %(levelname)s - %(message)s',  
        level=logging.DEBUG
    )    
else:
    logging.basicConfig(
        format='%(asctime)s.%(msecs).03d %(levelname)s - %(message)s', 
        level=logging.INFO
    )

def handle_sigint(signum, frame):
    logging.info("sigint received (%d)", signum)
    sys.exit(0)

def handle_sigterm(signum, frame):
    logging.warning("sigterm received (%d)", signum)
    sys.exit(0)

signal.signal(signal.SIGINT,  handle_sigint)
signal.signal(signal.SIGTERM, handle_sigterm)

def logHandler(level):

    def decorator(func):

        class LogHandler(logging.Handler):
            def emit(self, record):
                func(self.format(record))

        handler = LogHandler()
        handler.setLevel(level)

        logging.getLogger().addHandler(handler)

    return decorator
    
