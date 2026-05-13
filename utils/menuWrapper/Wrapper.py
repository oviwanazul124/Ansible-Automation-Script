import subprocess
from ansible_menus import *
import os

def clear():
    subprocess.run(["clear" if os.name == "posix" else "cls"], shell=True)


def menuWrapper(title, menuDict):
    while True:
        clear()
        print(f'--- {title} ---')
        for key, value in menuDict.items():
            print(f'{key}. {value['label']}')

        opt = input("\nSelect an option: ")

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
