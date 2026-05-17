# Custom Imports

from ansible_menus import menuMain
from utils.menuWrapper.Wrapper import menuWrapper

if __name__ == "__main__":
    try:
        menuWrapper(" Main Menu ", menuMain)
    except Exception as e:
        print(f"DEBUG: Error {e}")