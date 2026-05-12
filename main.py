# Custom Imports

from ansible_menus import menuMain
from utils.menuWrapper.Wrapper import menuWrapper

if __name__ == "__main__":
    menuWrapper("Ansible Menu", menuMain)