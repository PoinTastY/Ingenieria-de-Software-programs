from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import entities.figuras as figuras

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config(width=200, height=200)
        self.title("Avea figuras")

        self.lbBase = tk.Label(self, text="Ingrese Base")
        self.lbBase.place(x=10, y=10)
        self.txBase = tk.Entry(self)
        self.txBase.place(x=10, y=30)

        self.lbAltura = tk.Label(self, text="Ingrese Altura")
        self.lbAltura.place(x=10, y=60)
        self.txAltura = tk.Entry(self)
        self.txAltura.place(x=10, y=90)

        self.lbLados = None
        self.txLados = None

        self.optShape = ttk.Combobox(self, values=["Triangulo", "Cuadrado", "Rectangulo", "Poligono"])
        self.optShape.set("Triangulo")
        self.optShape.place(x=10, y=130)
        self.optShape.bind("<<ComboboxSelected>>", self.updateUI)  # Evento para actualizar la UI

        self.btCalcular = tk.Button(self, text="Calcular", command=self.btCalcularClicked)
        self.btCalcular.place(x=30, y=160)

    def updateUI(self, event):
        figura = self.optShape.get()
        
        # hide and clear stuff
        if self.lbLados:
            self.lbLados.place_forget()
        if self.txLados:
            self.txLados.place_forget()
        
        if figura == "Triangulo" or figura == "Rectangulo":
            self.lbBase.config(text="Ingrese Base")
            self.lbBase.place(x=10, y=10)
            self.txBase.place(x=10, y=30)

            self.lbAltura.config(text="Ingrese Altura")
            self.lbAltura.place(x=10, y=60)
            self.txAltura.place(x=10, y=90)
        elif figura == "Cuadrado":
            self.lbBase.config(text="Ingrese Lado")
            self.lbBase.place(x=10, y=10)
            self.txBase.place(x=10, y=30)

            self.lbAltura.place_forget()
            self.txAltura.place_forget()
        elif figura == "Poligono":
            self.lbBase.config(text="Ingrese Longitud de los lados")
            self.lbBase.place(x=10, y=10)
            self.txBase.place(x=10, y=30)

            self.lbLados = tk.Label(self, text="Número de lados")
            self.lbLados.place(x=10, y=60)
            self.txLados = tk.Entry(self)
            self.txLados.place(x=10, y=90)

    def btCalcularClicked(self):
        try:
            figura = self.optShape.get()

            if figura == "Triangulo":
                self.ob = figuras.triangulo(float(self.txBase.get()), float(self.txAltura.get()))
                self.ob.Calcular()

            elif figura == "Cuadrado":
                self.ob = figuras.cuadrado(float(self.txBase.get()))
                self.ob.Calcular()

            elif figura == "Rectangulo":
                self.ob = figuras.rectangulo(float(self.txBase.get()), float(self.txAltura.get()))
                self.ob.Calcular()

            elif figura == "Poligono":
                if(self.txLados.get() == "" or int(self.txLados.get()) < 5):
                    messagebox.showerror("Error", "Para calcular un polígono, debes ingresar un número de lados mayor o igual a 5")
                    return
                self.ob = figuras.poligono(float(self.txBase.get()), int(self.txLados.get()))
                self.ob.Calcular()
            else:
                messagebox.showerror("Error", "Seleccione una figura")
                return

            messagebox.showinfo("Área", "El área es: " + str(self.ob.getArea()))

        except ValueError as e:
            messagebox.showerror("Error", "Asegúrate de que todos los campos estén capturados: \n{}".format(e))

if __name__ == "__main__":
    app = App()
    app.mainloop()