# Imports

import logging
import logging.handlers
from pathlib import Path

def erHandler(error_message):

    loggingF(4, error_message)

    print("An error has occurred. Please check the logs for more details.")

    input("")

    exit(1)

# projectRoot function
# Objetive: Get the root path of the project.
# To ease the imports and use.

def projectRoot() -> Path:
    return Path(__file__).resolve().parents[2]

# getLogsDir function
# Objetive: Get the logs directory

def getLogsDir() -> Path:

    # Create the path of the log directory

    logsDir = projectRoot() / "logs"

    # Try to create the logs directory if it dosen't exists
    # and araise error if it fails

    try:

        logsDir.mkdir(parents=True, exist_ok=True)

    except Exception as e:

        print(f"Error creating logs directory: {e}")

    return logsDir

# setUpLogger function
# Objetive: Set up the logger with a 
# TimeRotation that packs the logs files
# to not overwrite the old logs

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
