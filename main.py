import tkinter as tk
from tkinter import font

def add(a, b):
    return a + b

def subtraction(a, b):
    return a - b

def multiplication(a, b):
    return a * b

def division(dividend, divisor):
    if divisor == 0:
        return "Error: Cannot divide by zero"
    return dividend / divisor

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("360x520")
        self.root.configure(bg="#dcdcdc")
        self.root.resizable(False, False)

        self.first = None
        self.operator = None
        self.current = ""

        self.create_fonts()
        self.create_display()
        self.create_buttons()

    def create_fonts(self):
        self.display_font = font.Font(size=18, weight="bold")
        self.result_font = font.Font(size=32, weight="bold")
        self.btn_font = font.Font(size=14, weight="bold")

    def create_display(self):
        frame = tk.Frame(self.root, bg="#eeeeee", height=120)
        frame.pack(fill="x", padx=12, pady=12)

        self.expr_label = tk.Label(
            frame, text="", anchor="e",
            bg="#eeeeee", fg="#777",
            font=self.display_font, padx=10
        )
        self.expr_label.pack(fill="x", pady=(10, 0))

        self.result_label = tk.Label(
            frame, text="0", anchor="e",
            bg="#eeeeee", fg="#444",
            font=self.result_font, padx=10
        )
        self.result_label.pack(fill="x")

    def create_buttons(self):
        frame = tk.Frame(self.root, bg="#dcdcdc")
        frame.pack(expand=True, fill="both", padx=12, pady=6)

        buttons = [
            ("7", "#777"), ("8", "#777"), ("9", "#777"), ("DEL", "#e74c3c"),
            ("4", "#777"), ("5", "#777"), ("6", "#777"), ("+", "#666"),
            ("1", "#777"), ("2", "#777"), ("3", "#777"), ("-", "#666"),
            (".", "#777"), ("0", "#777"), ("/", "#666"), ("x", "#666"),
        ]

        r = c = 0
        for text, color in buttons:
            self.make_button(frame, text, color, r, c)
            c += 1
            if c == 4:
                r += 1
                c = 0

        self.make_button(frame, "RESET", "#e74c3c", 4, 0, 2)
        self.make_button(frame, "=", "#3b44f6", 4, 2, 2)

    def make_button(self, parent, text, bg, r, c, span=1):
        btn = tk.Button(
            parent, text=text, bg=bg, fg="white",
            font=self.btn_font, bd=0,
            command=lambda t=text: self.press(t)
        )
        btn.grid(row=r, column=c, columnspan=span,
                 sticky="nsew", padx=4, pady=4, ipady=15)

        for i in range(4):
            parent.grid_columnconfigure(i, weight=1)
        for i in range(5):
            parent.grid_rowconfigure(i, weight=1)

    def press(self, key):
        if key.isdigit() or key == ".":
            self.current += key
            self.update()

        elif key in {"+", "-", "x", "/"}:
            if self.current:
                self.first = float(self.current)
                self.operator = key
                self.current = ""
                self.update()

        elif key == "=":
            if self.first is not None and self.operator and self.current:
                second = float(self.current)
                result = self.calculate(self.first, second, self.operator)
                self.result_label.config(text=result)
                self.first = None
                self.operator = None
                self.current = ""

        elif key == "DEL":
            self.current = self.current[:-1]
            self.update()

        elif key == "RESET":
            self.first = self.operator = None
            self.current = ""
            self.result_label.config(text="0")
            self.expr_label.config(text="")

    def calculate(self, a, b, op):
        if op == "+":
            return add(a, b)
        if op == "-":
            return subtraction(a, b)
        if op == "x":
            return multiplication(a, b)
        if op == "/":
            return division(a, b)

    def update(self):
        expr = f"{self.first or ''} {self.operator or ''} {self.current}"
        self.expr_label.config(text=expr.strip())
        self.result_label.config(text=self.current or "0")


if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()
