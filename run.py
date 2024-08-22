from config import *

import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        RotatingFileHandler(LOG_FILE, maxBytes=1000000, backupCount=1),
        logging.StreamHandler()
    ]
)


from app import app

if __name__ == '__main__':
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=DEBUG_MODE)