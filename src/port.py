import commands
from typing import Union

def get_num(question: str, err_msg: str, limit: (int, int), default: int) -> Union[int, commands.Quit]:
    while True:
        res = input(f"{question} (default: {default}): ").lower()
        if res == "q" or res == "quit":
            return commands.Quit()
        if res == "":
            return default
        try:
            res = int(res)
            if limit[0] <= res <= limit[1]:
                return res
        except:
            print(f"{err_msg}, try again or type 'quit' or 'q' to go back to the menu")

def get_port(default: int = 15000) -> Union[int, commands.Quit]:
    return get_num("Port", "Invalid port", (0, 65535), default)