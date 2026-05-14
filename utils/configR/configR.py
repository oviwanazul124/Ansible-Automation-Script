# Imports

import configparser
import os

# Custom Imports

from utils.logger.logger import loggingF

# Init configParser

config = configparser.ConfigParser()

# Paths to config.ini to solve bad imports

baseDir = os.path.dirname(os.path.abspath(__file__))
configPath = os.path.join(baseDir, '..', '..', 'config.ini')

# Read config.ini

filesRead = config.read(configPath)

# Exception to not reading .ini

if not filesRead:
    loggingF(4, f"No se pudo encontrar o leer el archivo config en: {configPath}")
    exit(1)

# configGet function
# Objetive: Get values of the config.ini

def configGet(sectionC, optionC):

    loggingF(1, f"Searching in config for section {sectionC} with value {optionC}")
    
    try:
        
        return config.get(sectionC, optionC)
    
    except configparser.NoSectionError:
        
        loggingF(4, f"The section [{sectionC}] dosen't exists in config.ini")
        
        raise
    
    except configparser.NoOptionError:
        
        loggingF(4, f"The option '{optionC}' dosen't exists for this [{sectionC}]")
        
        raise
