from colorama import init, Fore, Style

init(autoreset=True)


def success(msg):
    return f"{Fore.GREEN}{msg}{Style.RESET_ALL}"


def error(msg):
    return f"{Fore.RED}{msg}{Style.RESET_ALL}"


def warning(msg):
    return f"{Fore.YELLOW}{msg}{Style.RESET_ALL}"


def info(msg):
    return f"{Fore.CYAN}{msg}{Style.RESET_ALL}"


def confirm(msg):
    answer = input(f"{Fore.YELLOW}{msg} [y/N]: {Style.RESET_ALL}").strip().lower()
    return answer in ("y", "yes")
