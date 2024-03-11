import logging

logging.basicConfig(level='INFO',
    format='%(levelname)s %(filename)s: line %(lineno)d: message: %(message)s')
logger = logging.getLogger(__name__)