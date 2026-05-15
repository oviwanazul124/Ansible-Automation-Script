# Imports

import subprocess
import os

# Custom Imports

from utils.colors import Theme as T

# Banner

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
      
By Ovi (; ══ Version 1.0
      
"""
# clear function
# Objetive: Clear the terminal screen

def clear():
    subprocess.run(["clear" if os.name == "posix" else "cls"], shell=True)

# menuWrapper function
# Objetive: Handler the logic of the menu read from
# ansibel_menus.py

def menuWrapper(title, menuDict):

    import ansible_menus

    while True:

        clear()

        print(T.RED + BANNER + T.RESET)

        print(f"{T.BOLD}--- {title.upper()} ---{T.RESET}")

        print("══════════════════════════════════════════════════════════════════════════════════════")

        for key, value in menuDict.items():

            print(f'{key}. {value['label']}')

        print("══════════════════════════════════════════════════════════════════════════════════════")

        opt = input(f"\n{T.BOLD}Select an option » {T.RESET}")

        if opt in menuDict:

            item = menuDict[opt]

            if item['label'] in ['[Q] Exit', '[Q] Back to Main'] or item['func'] is None:
                
                break

            if item['func'] == 'debugMenu':

                menuWrapper("Debug Menu", ansible_menus.debugMenu)

            elif item['func'] == 'confMenu':

                menuWrapper("Configuration Menu", ansible_menus.confMenu)

            elif item['func'] == 'deployMenu':

                menuWrapper("Deploy Menu", ansible_menus.deployMenu)
            else:

                item['func']()

                input(f"\n{T.BOLD} Press Enter to continue » {T.RESET}")
        else:
            print(f"{T.GOLD} {T.BOLD} [X] Invalid option.Please try again. {T.RESET}")
            
            input()
