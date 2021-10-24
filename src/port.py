import commands
from typing import Union


def get_port(default: int = 15000) -> Union[int, commands.Quit]:
    while True:
        port = input(f"Port (default: {default}): ").lower()
        if port == "q" or port == "quit":
            return commands.Quit()
        if port == "":
            return default
        try:
            port = int(port)
            if 0 <= port <= 65535:
                return port
        except:
            print("Invalid port, try again")
