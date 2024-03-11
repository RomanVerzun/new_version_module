import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: %(filename)s:%(lineno)d: %(message)s'
)

logger = logging.getLogger(__name__)

logger.info('Это сообщение уровня INFO')