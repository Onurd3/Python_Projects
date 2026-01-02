import customtkinter as ctk
import math

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("360x450")
        self.resizable(False, False)
        self.configure(fg_color="black")  
        self.entry_var = ctk.StringVar()
        self.entry = ctk.CTkEntry(self, textvariable=self.entry_var,
                                  font=("Segoe UI", 28), justify="right", width=340, height=60)
        self.entry.pack(pady=15)
        self.buttons_frame = ctk.CTkFrame(self, fg_color="black")
        self.buttons_frame.pack()

        btns = [
            ["C", "⌫", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "√", "="],
        ]

        for r, row in enumerate(btns):
            for c, text in enumerate(row):
                if text == "=":
                    b = ctk.CTkButton(self.buttons_frame, text=text, width=80, height=60,
                                      fg_color="orange", hover_color="#ff9933",
                                      command=lambda t=text: self.on_click(t))
                else:
                    b = ctk.CTkButton(self.buttons_frame, text=text, width=80, height=60,
                                      fg_color="#1c1c1c", hover_color="#333333",
                                      command=lambda t=text: self.on_click(t))
                b.grid(row=r, column=c, padx=5, pady=5)

    def on_click(self, char):
        operators = "+-*/"
        if char == "C":
            self.entry_var.set("")
        elif char == "⌫":
            self.entry_var.set(self.entry_var.get()[:-1])
        elif char == "=":
            try:
                expr = self.entry_var.get().replace("√", "math.sqrt").replace("^", "**")
                expr = expr.replace("x²", "**2")

                for i in range(len(expr) - 1):
                    if expr[i] in operators and expr[i+1] in operators:
                        self.entry_var.set("Try again")
                        return

                result = eval(expr, {"__builtins__": None, "math": math})
                self.entry_var.set(str(result))
            except Exception:
                self.entry_var.set("")
        else:
            self.entry_var.set(self.entry_var.get() + char)


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
