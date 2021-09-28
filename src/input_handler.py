from commands import Command, Place, Surrender, Quit, Remove, Move, CommandType

class InputHandler:
    _surrender = None
    _quit = None
    _limits = None

    def __init__(self, surrendering="S", quitting="Q", limits=(0,23)):
        self._surrender = surrendering
        self._quit = quitting
        self._limits = limits

    def get_input(self, question: str, to_upper = True) -> str:
        response = input(question)
        while len(response) < 1:
            response = input(question)
        return response.upper( )if to_upper else response

    def make_question(self, cmd: CommandType) -> str:
        if cmd == CommandType.Remove:
            return "Remove piece [from] "
        elif cmd == CommandType.Move:
            return "Move piece [from, to] "
        elif cmd == CommandType.Place:
            return "Place coin [at] "
        return "unknown command "

    def get_command(self, cmd: CommandType) -> Command:
        response = self.get_input(self.make_question(cmd))
        if response == self._surrender:
            return Surrender()
        elif response == self._quit:
            return Quit()

        if cmd == CommandType.Place:
            try:
                number = int(response) - 1
                if self._limits[0] <= number <= self._limits[1]:
                    return Place(number)
                else:
                    print("Not a valid intersection, try again!")
                    return self.get_command(cmd)
            except:
                print("Not an intersection, try again!")
                return self.get_command(cmd)

        elif cmd == CommandType.Move:
            try:
                nums = list(map(lambda x: int(x) - 1, response.replace(',', ' ').split()))
                if len(nums) == 2:
                    if self._limits[0] <= nums[0] <= self._limits[1] and self._limits[0] <= nums[1] <= self._limits[1]:
                        return Move(nums[0], nums[1])
                    else:
                        print("Not an intersection within the limits, try again!")
                        return self.get_command(cmd)
                else:
                    print("Provide 2 intersections")
                    return self.get_command(cmd)
            except:
                print("Not intersections, try again!")
                return self.get_command(cmd)

        elif cmd == CommandType.Remove:
            try:
                number = int(response) - 1
                if self._limits[0] <= number <= self._limits[1]:
                    return Remove(number)
                else:
                    print("Not a valid intersection, try again!")
                    return self.get_command(cmd)
            except:
                print("Not an intersection, try again!")
                return self.get_command(cmd)


    def get_num(self, question: str) -> (int, str):
        response = input(question)
        try:
            number = int(response)
            return (number, "NUM")
        except:
            response = response.upper()
            if response in self._valids:
                return (0, response)
            else:
                return (0, self._invalid)

    def get_two_nums(self, question: str) -> ([int], str):
        response = input(question)
        try:
            numbers = list(map(lambda x: int(x), response.replace(',', ' ').split()))
            if len(numbers) == 2:
                return (numbers, "NUMS")
            else:
                return ([], "INVALID")
        except:
            response = response.upper()
            if response in self._valids:
                return ([], response)
            else:
                return (0, self._invalid)

    def get_input_keep_case(self, question: str) -> str:
        return input(question)

    def get_separated_input(self, question: str) -> [str]:
        response = input(question).upper()
        return list(filter(None, response.replace(",", " ").split()))
