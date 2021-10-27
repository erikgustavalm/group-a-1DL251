from commands import Command, Place, Surrender, Exit, Remove, Move, CommandType
import os
from typing import Union

def flush_input():
    if os.name == 'nt':
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    elif os.name == 'posix':
        import sys, termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

class InputHandler:
    _surrender = None
    _exit = None
    _limits = None
    _quit = None

    def __init__(self,
                 surrendering=["S", "SURRENDER"],
                 exiting=["E", "EXIT"],
                 quitting=["Q", "Quit"],
                 limits=(0, 23)):
        self._surrender = surrendering
        self._exit = exiting
        self._limits = limits
        self._quit = quitting

    def get_input(self, question: str, to_upper=True) -> Union[str, Exit]:
        while True:
            flush_input()
            response = input(question)
            if response.upper() in self._exit:
                return Exit()
            elif response.upper() in self._quit:
                exit()
            if len(response) >= 1:
                break
            print(f"   Name needs to be at least 1 character long. Try again!")
        return response.upper() if to_upper else response

    def _make_question(self, cmd: CommandType) -> str:
        if cmd == CommandType.Remove:
            return "   Remove piece [from] "
        elif cmd == CommandType.Move:
            return "   Move piece [from, to] "
        elif cmd == CommandType.Place:
            return "   Place coin [at] "
        return "   unknown command "

    def get_command(self, cmd: CommandType) -> Command:
        response = self.get_input(self._make_question(cmd))
        if isinstance(response, Exit):
            return Exit()
        elif response in self._surrender:
            return Surrender()

        if cmd == CommandType.Place:
            try:
                number = int(response) - 1
                if self._limits[0] <= number <= self._limits[1]:
                    return Place(number)
                else:
                    print(f"   [ Not a valid intersection, valid values are between {self._limits[0]+1} and {self._limits[1]+1}, inclusive. Try again! ]")
                    return self.get_command(cmd)
            except:
                print(f"   [ Not an intersection, valid values are numbers between {self._limits[0]+1} and {self._limits[1]+1}, inclusive. Try again! ]")
                return self.get_command(cmd)

        elif cmd == CommandType.Move:
            try:
                nums = list(map(lambda x: int(x) - 1,
                            response.replace(',', ' ').split()))
                if len(nums) == 2:
                    if (self._limits[0] <= nums[0] <= self._limits[1]
                            and self._limits[0] <= nums[1] <= self._limits[1]):
                        return Move(nums[0], nums[1])
                    else:
                        print(f"   [ Not an intersection within the limits, valid values are between {self._limits[0]+1} and {self._limits[1]+1}, inclusive. try again! ]")
                        return self.get_command(cmd)
                else:
                    print("   [ Provide 2 intersections ]")
                    return self.get_command(cmd)
            except:
                print(f"   [ Not intersections, valid values are two numbers between {self._limits[0]+1} and {self._limits[1]+1}, inclusive. Try again! ]")
                return self.get_command(cmd)

        elif cmd == CommandType.Remove:
            try:
                number = int(response) - 1
                if self._limits[0] <= number <= self._limits[1]:
                    return Remove(number)
                else:
                    print(f"   [ Not a valid intersection, valid values are between {self._limits[0]+1} and {self._limits[1]+1}, inclusive. Try again! ]")
                    return self.get_command(cmd)
            except:
                print(f"   [ Not an intersection, valid values are numbers between {self._limits[0]+1} and {self._limits[1]+1}, inclusive. Try again! ]")
                return self.get_command(cmd)
