import logging


_Logger = logging.getLogger('_log_.event')


def info(msg):
    _Logger.info(msg)
