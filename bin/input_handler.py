class InputHandler():
    def get_input(self, question: str) -> [str]:
        response = input(question)
        return response.replace(",", " ").split(" ")
