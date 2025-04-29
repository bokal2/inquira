import logging
from pythonjsonlogger import jsonlogger
import sys


def setup_logging():
    try:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        log_handler = logging.StreamHandler(sys.stdout)
        log_handler.setLevel(logging.INFO)

        formatter = jsonlogger.JsonFormatter(
            fmt=(
                "%(asctime)s %(levelname)s %(name)s %(message)s "
                "%(pathname)s %(lineno)d %(threadName)s"
            )
        )
        log_handler.setFormatter(formatter)

        # Clearing any existing handlers first
        logger.handlers = []
        logger.addHandler(log_handler)

        # Setting SQLAlchemy engine logs to INFO as well
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

    except Exception as e:
        print(f"Logging setup failed: {str(e)}")
