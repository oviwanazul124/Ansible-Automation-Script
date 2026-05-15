# Imports

import subprocess
import os

# Custom Imports

from ansible_menus import *

#

BANNER = r"""

 ▄▄▄       ███▄    █   ██████  ██▓ ▄▄▄▄    ██▓    ▓█████     ▄▄▄       █    ██ ▄▄▄█████▓ ▒█████   ███▄ ▄███▓ ▄▄▄     ▄▄▄█████▓ ██▓ ▒█████   ███▄    █ 
▒████▄     ██ ▀█   █ ▒██    ▒ ▓██▒▓█████▄ ▓██▒    ▓█   ▀    ▒████▄     ██  ▓██▒▓  ██▒ ▓▒▒██▒  ██▒▓██▒▀█▀ ██▒▒████▄   ▓  ██▒ ▓▒▓██▒▒██▒  ██▒ ██ ▀█   █ 
▒██  ▀█▄  ▓██  ▀█ ██▒░ ▓██▄   ▒██▒▒██▒ ▄██▒██░    ▒███      ▒██  ▀█▄  ▓██  ▒██░▒ ▓██░ ▒░▒██░  ██▒▓██    ▓██░▒██  ▀█▄ ▒ ▓██░ ▒░▒██▒▒██░  ██▒▓██  ▀█ ██▒
░██▄▄▄▄██ ▓██▒  ▐▌██▒  ▒   ██▒░██░▒██░█▀  ▒██░    ▒▓█  ▄    ░██▄▄▄▄██ ▓▓█  ░██░░ ▓██▓ ░ ▒██   ██░▒██    ▒██ ░██▄▄▄▄██░ ▓██▓ ░ ░██░▒██   ██░▓██▒  ▐▌██▒
 ▓█   ▓██▒▒██░   ▓██░▒██████▒▒░██░░▓█  ▀█▓░██████▒░▒████▒    ▓█   ▓██▒▒▒█████▓   ▒██▒ ░ ░ ████▓▒░▒██▒   ░██▒ ▓█   ▓██▒ ▒██▒ ░ ░██░░ ████▓▒░▒██░   ▓██░
 ▒▒   ▓▒█░░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░░▓  ░▒▓███▀▒░ ▒░▓  ░░░ ▒░ ░    ▒▒   ▓▒█░░▒▓▒ ▒ ▒   ▒ ░░   ░ ▒░▒░▒░ ░ ▒░   ░  ░ ▒▒   ▓▒█░ ▒ ░░   ░▓  ░ ▒░▒░▒░ ░ ▒░   ▒ ▒ 
  ▒   ▒▒ ░░ ░░   ░ ▒░░ ░▒  ░ ░ ▒ ░▒░▒   ░ ░ ░ ▒  ░ ░ ░  ░     ▒   ▒▒ ░░░▒░ ░ ░     ░      ░ ▒ ▒░ ░  ░      ░  ▒   ▒▒ ░   ░     ▒ ░  ░ ▒ ▒░ ░ ░░   ░ ▒░
  ░   ▒      ░   ░ ░ ░  ░  ░   ▒ ░ ░    ░   ░ ░      ░        ░   ▒    ░░░ ░ ░   ░      ░ ░ ░ ▒  ░      ░     ░   ▒    ░       ▒ ░░ ░ ░ ▒     ░   ░ ░ 
      ░  ░         ░       ░   ░   ░          ░  ░   ░  ░         ░  ░   ░                  ░ ░         ░         ░  ░         ░      ░ ░           ░ 

══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
      
By Oviwanazul124 ══ Version 1.0
      
"""

RED = '\033[31m'
RESET = '\033[0m'
BOLD = '\033[1m'

# clear function
# Objetive: Clear the terminal screen

def clear():
    subprocess.run(["clear" if os.name == "posix" else "cls"], shell=True)

# menuWrapper function
# Objetive: Handler the logic of the menu read from
# ansibel_menus.py

def menuWrapper(title, menuDict):

    while True:

        clear()

        print(RED + BANNER + RESET)

        print(f"{BOLD}--- {title.upper()} ---{RESET}")

        print("══════════════════════════════════════════════════════════════════════════════════════")

        for key, value in menuDict.items():

            print(f'{key}. {value['label']}')

        print("══════════════════════════════════════════════════════════════════════════════════════")

        opt = input(f"\n{BOLD}Select an option » {RESET}")

        if opt in menuDict:

            item = menuDict[opt]

            if item['label'] in ['Exit', 'Back to Main'] or item['func'] is None:
                
                break

            if item['func'] == 'debugMenu':

                menuWrapper("Debug Menu", debugMenu)

            elif item['func'] == 'confMenu':

                menuWrapper("Configuration Menu", confMenu)

            elif item['func'] == 'deployMenu':

                menuWrapper("Deploy Menu", deployMenu)
            else:

                item['func']()

                input("\nPress Enter to continue...")
        else:
            print("Invalid option.Please try again.")
            
            input()
