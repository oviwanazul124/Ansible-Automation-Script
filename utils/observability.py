# Imports

from pathlib import Path
import logging
from paths import logsDir_path, logs_dir

# getLogsDir function
# Objetive: Get the logs directory

def getLogsDir() -> Path:

    try:

        logsDir_path.mkdir(parents=True, exist_ok=True)

    except Exception as e:

        print(f"Error creating logs directory: {e}")

# setUpLogger function
# Objetive: Set up the logger with a 
# TimeRotation that packs the logs files
# to not overwrite the old logs

def setUpLogger():


    logger = logging.getLogger("logger")

    logger.setLevel(logging.DEBUG)

    handler = logging.handlers.TimedRotatingFileHandler(
        logs_dir, when="midnight", interval=1 ,backupCount=7, encoding="utf-8"
    )

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    handler.setFormatter(formatter)

    if not logger.handlers:
        
        logger.addHandler(handler)

    return logger

logger= setUpLogger()

# loggingF function
# Objetive: Created to be called in others parts of the 
# script

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

def erHandler(error_message):

    loggingF(4, error_message)

    print("An error has occurred. Please check the logs for more details.")

    input("")

    exit(1)