from tkinter import font, ttk
import tkinter as tk
from tkinter import messagebox
from math import log, sqrt, factorial

from application.converters import *

class App (tk.Tk):
    def __init__(self):
        super().__init__()
        self.config(width=420, height=600)
        self.title("Calculadora Mamalona")
        self.build_interface()

    def build_interface(self) -> None:
        titlefont = font.Font(family="Helvetica", size=20)
        self.display = tk.Entry(self, width=16, font=titlefont)
        self.display.grid(row=0, column=0, columnspan=5)

        self.conversion_frame = tk.Frame(self)
        self.conversion_frame.grid(row=1, column=0, columnspan=5, sticky="ew")

        self.update_conversion(0)#conversion labels

        buttons = [
            ('A', self.btnAClicked), ('^', self.btnPowerClicked), ('log', self.btnLogClicked), ('CE', self.btnCEClicked), ('<-', self.btnPopClicked),
            ('B', self.btnBClicked), ('√', self.btnRootClicked), ('n!', self.btnNotClicked), ('%', self.btnModuleClicked), ('/', self.btnDivClicked),
            ('C', self.btnCClicked), ('7', self.btn7Clicked), ('8', self.btn8Clicked), ('9', self.btn9Clicked), ('*', self.btnMultClicked),
            ('D', self.btnDClicked), ('4', self.btn4Clicked), ('5', self.btn5Clicked), ('6', self.btn6Clicked), ('-', self.btnSubClicked),
            ('E', self.btnEClicked), ('1', self.btn1Clicked), ('2', self.btn2Clicked), ('3', self.btn3Clicked), ('+', self.btnAddClicked),
            ('!=', self.btnNotEqualClicked), ('Abs', self.btnAbsoluteClicked), ('0', self.btn0Clicked), ('.', self.btnDotClicked), ('=', self.btnEqualClicked)
        ]

        row = 5
        col = 0
        for (text, command) in buttons:
            tk.Button(self, text=text, command=command, width=6).grid(row=row, column=col, padx=3, pady=3)
            col += 1
            if col > 4:
                col = 0
                row += 1

    def btnAClicked(self):
        self.display.insert(tk.END, 'A')

    def btnPowerClicked(self):
        value = self.get_current_value()
        self.display.insert(tk.END, '**')

    def btnLogClicked(self):
        value = self.get_current_value()
        result = log(value)
        self.set_display_value(result)

    def btnCEClicked(self):
        self.display.delete(0, tk.END)
        self.update_conversion(0)

    def btnPopClicked(self):
        current_text = self.display.get()
        if current_text:
            self.display.delete(len(current_text) - 1)

    def btnBClicked(self):
        self.display.insert(tk.END, 'B')

    def btnRootClicked(self):
        value = self.get_current_value()
        result = sqrt(value)
        self.set_display_value(result)

    def btnNotClicked(self):
        value = self.get_current_value()
        result = factorial(int(value))
        self.set_display_value(result)

    def btnModuleClicked(self):
        self.display.insert(tk.END, '%')

    def btnDivClicked(self):
        self.display.insert(tk.END, '/')

    def btnCClicked(self):
        self.display.insert(tk.END, 'C')

    def btn7Clicked(self):
        self.display.insert(tk.END, '7')

    def btn8Clicked(self):
        self.display.insert(tk.END, '8')

    def btn9Clicked(self):
        self.display.insert(tk.END, '9')

    def btnMultClicked(self):
        self.display.insert(tk.END, '*')

    def btnDClicked(self):
        self.display.insert(tk.END, 'D')

    def btn4Clicked(self):
        self.display.insert(tk.END, '4')

    def btn5Clicked(self):
        self.display.insert(tk.END, '5')

    def btn6Clicked(self):
        self.display.insert(tk.END, '6')

    def btnSubClicked(self):
        self.display.insert(tk.END, '-')

    def btnEClicked(self):
        self.display.insert(tk.END, 'E')

    def btn1Clicked(self):
        self.display.insert(tk.END, '1')

    def btn2Clicked(self):
        self.display.insert(tk.END, '2')

    def btn3Clicked(self):
        self.display.insert(tk.END, '3')

    def btnAddClicked(self):
        self.display.insert(tk.END, '+')

    def btnNotEqualClicked(self):
        self.display.insert(tk.END, '!=')

    def btnAbsoluteClicked(self):
        value = self.get_current_value()
        result = abs(value)
        self.set_display_value(result)

    def btn0Clicked(self):
        self.display.insert(tk.END, '0')

    def btnDotClicked(self):
        self.display.insert(tk.END, '.')

    def btnEqualClicked(self):
        try:
            
            if(self.display.get() == "9+10"):
                messagebox.showinfo("Resultado", "21")
                self.btnCEClicked()
                return
            result = eval(self.display.get())
            self.set_display_value(result)
            self.update_conversion(result)
        except Exception as e:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "Syntax Error")

    def get_current_value(self):
        try:
            return float(self.display.get())
        except ValueError:
            return 0.0

    def set_display_value(self, value):
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, str(value))
        self.update_conversion(float(value))


    def clear_labels(self):
        if hasattr(self, 'lblHex') and self.lblHex is not None:
            self.lblHex.destroy()
        if hasattr(self, 'lblDec') and self.lblDec is not None:
            self.lblDec.destroy()
        if hasattr(self, 'lblOct') and self.lblOct is not None:
            self.lblOct.destroy()
        if hasattr(self, 'lblBin') and self.lblBin is not None:
            self.lblBin.destroy()

    def update_conversion(self, value):

        for widget in self.conversion_frame.winfo_children():
            widget.destroy()

        self.lblHex = tk.Label(self.conversion_frame, text=f"Hex: {Dec_Hex(value)}", anchor="w")
        self.lblHex.grid(row=0, column=0, columnspan=5, sticky="w")

        self.lblDec = tk.Label(self.conversion_frame, text=f"Dec: {str(value)}", anchor="w")
        self.lblDec.grid(row=1, column=0, columnspan=5, sticky="w")

        self.lblOct = tk.Label(self.conversion_frame, text=f"Oct: {Dec_Oct(value)}", anchor="w")
        self.lblOct.grid(row=2, column=0, columnspan=5, sticky="w")

        self.lblBin = tk.Label(self.conversion_frame, text=f"Bin: {Dec_Bin(value)}", anchor="w")
        self.lblBin.grid(row=3, column=0, columnspan=5, sticky="w")


if __name__ == "__main__":
    app = App()
    app.mainloop()