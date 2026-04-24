import logging
import logging.handlers
from pathlib import Path
from datetime import datetime

def projectRoot() -> Path:
    return Path(__file__).resolve().parents[2]

def getLogsDir() -> Path:
    logsDir = projectRoot() / "logs"
    logsDir.mkdir(parents=True, exist_ok=True)
    return logsDir

def setUpLogger():
    logsDir = getLogsDir()
    logFile = logsDir / f"log.log"

    logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)

    handler = logging.handlers.TimedRotatingFileHandler(
        logFile, when="midnight", interval=1 ,backupCount=7, encoding="utf-8"
    )

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger

logger= setUpLogger()

def loggingF(type, string):

    match type:
        case 1:
            logger.debug(string)
        case 2:
            logger.info(string)
        case 3:
            logger.warning(string)
        case 4:
            logger.error(string)
        case _:
            logger.error("Logger is not working")
