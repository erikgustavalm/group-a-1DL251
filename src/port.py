import commands
from typing import Union

def get_num(question: str, err_msg: str, limit: (int, int), default: int) -> Union[int, commands.Exit]:
    while True:
        res = input(f"{question} (default: {default}): ").lower()
        if res == "e" or res == "exit":
            return commands.Exit()
        if res == "q" or res == "quit":
            exit()
        if res == "":
            return default
        try:
            res = int(res)
            if limit[0] <= res <= limit[1]:
                return res
            else:
                print(f"{err_msg}, try again or type 'exit' or 'e' to go back to the menu")
                print(f"valid inputs are between {limit[0]} and {limit[0]}, inclusive.\n")
        except:
            print(f"valid inputs are between {limit[0]} and {limit[0]}, inclusive.\n")
            print(f"{err_msg}, try again or type 'exit' or 'e' to go back to the menu")

def get_port(default: int = 15000) -> Union[int, commands.Exit]:
    return get_num("Port", "Invalid port", (0, 65535), default)