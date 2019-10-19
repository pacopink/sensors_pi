#!/bin/env python
#coding: utf8


### 准备日志 ###
import logging
DEBUG=logging.DEBUG
INFO=logging.INFO
WARN=logging.WARN
ERROR=logging.ERROR
CRITICAL=logging.CRITICAL

log_debug = logging.debug
log_info = logging.info
log_warn = logging.warn
log_error = logging.error
log_critical = logging.critical

FORMAT = '%(asctime)-15s#%(process)d#%(levelname)s#%(lineno)d@%(filename)s# %(message)s'

logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.setLevel(DEBUG)


def setLevel(lvl):
    logger.setLevel(lvl)
