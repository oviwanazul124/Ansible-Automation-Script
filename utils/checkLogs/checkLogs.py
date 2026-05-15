# Imports

import time

# Custom Imports

from utils.colors import Theme as T

def Checklog(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as f:
            f.seek(0, 2)
            while True:
                linea = f.readline()
                if not linea:
                    time.sleep(0.1)
                    continue
                print(linea, end='')
    except KeyboardInterrupt:
        print(f"\n{T.BOLD} [!] Logs check interrupted by keyboard {T.RESET}")