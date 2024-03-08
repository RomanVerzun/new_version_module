import logging

logging.basicConfig(filename='app.log', filemode='w', level=logging.DEBUG,
                    format='%(name)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

logger = logging.getLogger(__name__)

logger.debug("Debug")
logger.info("INFO")
logger.warning("Warning")
logger.error("ERROR")
logger.critical("CRITICAL")