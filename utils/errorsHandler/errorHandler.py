# Custom Imports

from utils.logger.logger import loggingF

def erHandler(error_message):

    loggingF(4, error_message)

    print("An error has occurred. Please check the logs for more details.")

    input("")

    exit(1)