# utils/colors.py

class Theme:
    # Text Styles
    RESET = "\033[0m"
    BOLD  = "\033[1m"
    UNLN  = "\033[4m"

    RED       = "\033[38;5;196m" # Intense Red
    DARK_RED  = "\033[31m"       # Standard Red
    GREY      = "\033[38;5;244m" # For secondary text
    GOLD      = "\033[38;5;214m" # For highlights/warnings
    GREEN     = "\033[38;5;82m"  # For success messages
    CYAN      = "\033[36m"       # For borders