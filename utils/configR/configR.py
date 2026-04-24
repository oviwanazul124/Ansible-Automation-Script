import configparser
from utils.logger.logger import loggingF

config = configparser.ConfigParser()

try:
    config.read('config.ini')
except configparser.Error as e:
    loggingF(4, f"There was a error parsing the config.ini it was {e}")
    print("There was an error check the log for more info")
    exit(1)

def configGet(sectionC, optionC):

    loggingF(1, f"Searching in config for section {sectionC} with value {optionC}")
    value = config.get(sectionC, optionC)
    return value