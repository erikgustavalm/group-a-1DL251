class InputHandler:
    def get_input(self, question: str) -> [str]:
        response = input(question).upper()
        return response.replace(",", " ").split(" ")
