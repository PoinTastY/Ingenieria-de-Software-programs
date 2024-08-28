from tkinter import ttk
import tkinter as tk
from tkinter import messagebox

class App (tk.Tk):
    def __init__(self):
        super().__init__()
        self.config(width=420, height=600)
        self.title("Calculadora Mamalona")
        self.build_btns()

    def build_btns(self) -> None:
            self.display = tk.Entry(self).grid(row=0, column=0, rowspan=5)
            self.lblHex = tk.Label(self, text="Hex").grid(row=1, column=0, rowspan=5)
            self.lblDec = tk.Label(self, text="Dec").grid(row=2, column=0, rowspan=5)
            self.lblOct = tk.Label(self, text="Oct").grid(row=3, column=0, rowspan=5)
            self.lblBin = tk.Label(self, text="Bin").grid(row=4, column=0, rowspan=5)

            self.btnA = tk.Button(self, text="A", command=self.btnAClicked).grid(row=5, column=0)
            self.btnPower = tk.Button(self, text="^", command=self.btnPowerClicked).grid(row=5, column=1)
            self.btnLog = tk.Button(self, text="log", command=self.btnLogClicked).grid(row=5, column=2)
            self.btnCE = tk.Button(self, text="CE", command=self.btnCEClicked).grid(row=5, column=3)
            self.btnPop = tk.Button(self, text="<-", command=self.btnPopClicked).grid(row=5, column=4)

            self.btnB = tk.Button(self, text="B", command=self.btnBClicked).grid(row=6, column=0)
            self.btnRoot = tk.Button(self, text="√", command=self.btnRootClicked).grid(row=6, column=1)
            self.btnNot = tk.Button(self, text="n!", command=self.btnNotClicked).grid(row=6, column=2)
            self.btnModule = tk.Button(self, text="%", command=self.btnModuleClicked).grid(row=6, column=3)
            self.btnDiv = tk.Button(self, text="/", command=self.btnDivClicked).grid(row=6, column=4)

            self.btnC = tk.Button(self, text="C", command=self.btnCClicked).grid(row=7, column=0)
            self.btn7 = tk.Button(self, text="7", command=self.btn7Clicked).grid(row=7, column=1)
            self.btn8 = tk.Button(self, text="8", command=self.btn8Clicked).grid(row=7, column=2)
            self.btn9 = tk.Button(self, text="9", command=self.btn9Clicked).grid(row=7, column=3)
            self.btnMult = tk.Button(self, text="*", command=self.btnMultClicked).grid(row=7, column=4)

            self.btnD = tk.Button(self, text="D", command=self.btnDClicked).grid(row=8, column=0)
            self.btn4 = tk.Button(self, text="4", command=self.btn4Clicked).grid(row=8, column=1)
            self.btn5 = tk.Button(self, text="5", command=self.btn5Clicked).grid(row=8, column=2)
            self.btn6 = tk.Button(self, text="6", command=self.btn6Clicked).grid(row=8, column=3)
            self.btnSub = tk.Button(self, text="-", command=self.btnSubClicked).grid(row=8, column=4)

            self.btnE = tk.Button(self, text="E", command=self.btnEClicked).grid(row=9, column=0)
            self.btn1 = tk.Button(self, text="1", command=self.btn1Clicked).grid(row=9, column=1)
            self.btn2 = tk.Button(self, text="2", command=self.btn2Clicked).grid(row=9, column=2)
            self.btn3 = tk.Button(self, text="3", command=self.btn3Clicked).grid(row=9, column=3)
            self.btnAdd = tk.Button(self, text="+", command=self.btnAddClicked).grid(row=9, column=4)

            self.btnNotEqual = tk.Button(self, text="!=", command=self.btnNotEqualClicked).grid(row=10, column=0)
            self.btnAbsolute = tk.Button(self, text="Abs", command=self.btnAbsoluteClicked).grid(row=10, column=1)
            self.btn0 = tk.Button(self, text="0", command=self.btn0Clicked).grid(row=10, column=2)
            self.btnDot = tk.Button(self, text=".", command=self.btnDotClicked).grid(row=10, column=3)
            self.btnEqual = tk.Button(self, text="=", command=self.btnEqualClicked).grid(row=10, column=4)

    def btnAClicked():
         


if __name__ == "__main__":
    app = App()
    app.mainloop()