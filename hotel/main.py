import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from data.data_repo import cargar_datos
from presentation.clientestab import ClientesTab
from presentation.reservacionestab import ReservacionesTab
from presentation.habitacionestab import HabitacionTab


class SistemaReservaciones(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Reservaciones")
        self.geometry("600x400")

        try:
            self.data_repo = cargar_datos()
        except ValueError as e:
            messagebox.showerror("Error", "no se puede leer el json que contiene los datos: " + str(e))
            self.data_repo = None

        # Crear un widget de pestañas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # Crear las pestañas
        self.clientes_tab = ClientesTab(self.notebook, self.data_repo)
        self.reservaciones_tab = ReservacionesTab(self.notebook, self.data_repo)
        self.habitacion_tab = HabitacionTab(self.notebook, self.data_repo)

        # Añadir pestañas al notebook
        self.notebook.add(self.clientes_tab, text="Clientes")
        self.notebook.add(self.reservaciones_tab, text="Reservaciones")
        self.notebook.add(self.habitacion_tab, text="Habitación")




if __name__ == "__main__":
    app = SistemaReservaciones()
    app.mainloop()
