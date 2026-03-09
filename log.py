import logging
from logging.handlers import SysLogHandler, RotatingFileHandler
from os import makedirs
from sys import platform

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if platform.startswith('linux'):
    syslog_handler = SysLogHandler(address='/dev/log')
    logger.addHandler(syslog_handler)

makedirs('logs', exist_ok=True)
file_handler = RotatingFileHandler('logs/audit.log')
logger.addHandler(file_handler)
