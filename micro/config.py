# -*- coding: utf-8 -*

from datetime import datetime

import dataset
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

CONFIG_URL = os.getenv('CONFIG_URL') or "sqlite:///mydatabase.db"

db = dataset.connect(CONFIG_URL)
table = db['config']

##
#

def get(name, default=None, type=None):
    res = table.find_one(name=name)
    
    if res is None:
        return default
    
    value = res['value']
    
    if type is datetime:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
    
    return value

##
#

def set(name, value):
    data = dict(name=name, value=str(value))
    table.upsert(data, ['name'])
 
