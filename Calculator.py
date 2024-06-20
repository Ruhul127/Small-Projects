# calculator_game.py

import tkinter as tk
from random import randint, choice

class CalculatorGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Calculator Game")

        self.num1_label = tk.Label(self.window, text="", font=("Arial", 24))
        self.num1_label.pack()

        self.num2_label = tk.Label(self.window, text="", font=("Arial", 24))
        self.num2_label.pack()

        self.operator_label = tk.Label(self.window, text="", font=("Arial", 24))
        self.operator_label.pack()

        self.answer_entry = tk.Entry(self.window, font=("Arial", 24), width=10)
        self.answer_entry.pack()

        self.check_button = tk.Button(self.window, text="Check", command=self.check_answer)
        self.check_button.pack()

        self.score_label = tk.Label(self.window, text="Score: 0", font=("Arial", 24))
        self.score_label.pack()

        self.score = 0
        self.generate_question()

        self.window.mainloop()

    def generate_question(self):
        self.num1 = randint(1, 10)
        self.num2 = randint(1, 10)
        self.operator = choice(["+", "-", "*"])
        self.answer = self.calculate_answer()

        self.num1_label.config(text=str(self.num1))
        self.num2_label.config(text=str(self.num2))
        self.operator_label.config(text=self.operator)

    def calculate_answer(self):
        if self.operator == "+":
            return self.num1 + self.num2
        elif self.operator == "-":
            return self.num1 - self.num2
        else:
            return self.num1 * self.num2

    def check_answer(self):
        user_answer = int(self.answer_entry.get())
        if user_answer == self.answer:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.generate_question()
        else:
            self.score_label.config(text=f"Score: {self.score} (Incorrect)")

if __name__ == "__main__":
    game = CalculatorGame()