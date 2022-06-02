from distutils.log import WARN


GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
ENDC = "\033[0m"
WARNING = "[" + YELLOW + "*" + ENDC + "]"
ERROR = "[" + RED + "*" + ENDC + "]"
NOTICE = "[" + GREEN + "*" + ENDC + "]"


def colorize(text: str, color) -> str:
    return color + text + ENDC


def warning(text: str) -> None:
    print(WARNING + " " + text)


def error(text: str) -> None:
    print(ERROR + " " + text)


def notice(text: str) -> None:
    print(NOTICE + " " + text)
