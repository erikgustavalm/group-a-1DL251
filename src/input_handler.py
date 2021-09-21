class InputHandler:
    def get_input(self, question: str) -> [str]:
        return input(question).upper()

    def get_input_keep_case(self, question: str) -> [str]:
        return input(question)

    def get_separated_input(self, question: str) -> [str]:
        response = input(question).upper()
        return response.replace(",", " ").split(" ")