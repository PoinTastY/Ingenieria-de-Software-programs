from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import entities.figuras as figuras

class App (tk.Tk):
    def __init__(self):
        super().__init__()
        self.config(width=300, height=300)
        self.title("Avea figuras")
        self.lbBase = tk.Label(self, text="Ingrese Base")
        self.lbBase.place(x=10, y=10)
        self.txBase = tk.Entry(self)
        self.txBase.place(x=10, y=30)
        self.lbAltura = tk.Label(self, text="Ingrese Altura")   
        self.lbAltura.place(x=10, y=60)
        self.txAltura = tk.Entry(self)
        self.txAltura.place(x=10, y=90)
        self.optShape = ttk.Combobox(self, values=["Triangulo", "Cuadrado", "Rectangulo", "Poligono"])
        self.optShape.set("Triangulo")
        self.optShape.place(x=10, y=130)
        self.btCalcular = tk.Button(self, text="Calcular", command=self.btCalcularClicked)
        self.btCalcular.place(x=30, y=160)

    def btCalcularClicked(self):
        try:
            if(self.optShape.get() == "Triangulo"):
                self.ob = figuras.triangulo(float(self.txBase.get()), float(self.txAltura.get()))
                self.ob.Calcular()

            elif(self.optShape.get() == "Cuadrado"):
                self.ob = figuras.cuadrado(float(self.txBase.get()))
                self.ob.Calcular()

            elif(self.optShape.get() == "Rectangulo"):
                self.ob = figuras.rectangulo(float(self.txBase.get()), float(self.txAltura.get()))
                self.ob.Calcular()
            
            elif(self.optShape.get() == "Poligono"):
                self.ob = figuras.poligono(float(self.txBase.get()), float(self.txAltura.get()))
                self.ob.Calcular()
            else:
                messagebox.showerror("Error", "Seleccione una figura")
                return

            messagebox.showinfo("Area", "El area es: " + str(self.ob.getArea()))

        except ValueError as e:
            messagebox.showerror("Error", "Asegurate de que todos los campos esten capturados: \n{}".format(e))

if __name__ == "__main__":
    app = App()
    app.mainloop()
