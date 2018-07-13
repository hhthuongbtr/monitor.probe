from os import path, remove
import logging
import logging.config
import logging.handlers
import json
from config.config import LOGGING as logging_config_dict

from .agent import Agent
from .log import Log
from .profile import Profile, Snmp

# Create the Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

# Create the Handler for logging data to a file
logger_handler = logging.handlers.SysLogHandler(address = '/dev/log')
logger_handler.setLevel(logging.WARNING)

# Create a Formatter for formatting the log messages
logger_formatter = logging.Formatter('Monitor: date: %(asctime)s - serverity: %(levelname)s - message: %(message)s')

# Add the Formatter to the Handler
logger_handler.setFormatter(logger_formatter)

# Add the Handler to the Logger
logger.addHandler(logger_handler)
logger.info('Completed configuring logger()!')

