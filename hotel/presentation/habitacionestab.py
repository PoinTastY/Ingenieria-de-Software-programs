from tkinter import ttk
import tkinter as tk
from data.data_repo import agregar_habitacino, buscar_habitacion
from entities.habitacion import *
from tkinter import messagebox


class HabitacionTab(ttk.Frame):
    def __init__(self, parent, data):
        self.data = data
        super().__init__(parent)

        # Labels y Entradas para buscar y detalles de la habitación
        ttk.Label(self, text="Ingrese Numero de Habitación:").grid(row=0, column=0, padx=5, pady=5)
        self.numero_busqueda = ttk.Entry(self)
        self.numero_busqueda.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self, text="Buscar", command = self.BtnSearchClicked).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(self, text="Habitacion ID:").grid(row=1, column=0, padx=5, pady=5)
        self.habitacion_id_entry = ttk.Entry(self)
        self.habitacion_id_entry.insert(0, self.data['indices']['habitaciones'] + 1)
        self.habitacion_id_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="Numero:").grid(row=2, column=0, padx=5, pady=5)
        self.numero_entry = ttk.Entry(self)
        self.numero_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text="Seleccione Estado Habitacion:").grid(row=3, column=0, padx=5, pady=5)
        self.estado_combobox = ttk.Combobox(self, values=["Libre", "Ocupada"])
        self.estado_combobox.grid(row=3, column=1, padx=5, pady=5)

        # Botones de control
        self.botones_frame = ttk.Frame(self)
        self.botones_frame.grid(row=4, column=0, columnspan=3, pady=10)

        ttk.Button(self.botones_frame, text="Nueva Habitación", command=self.BtnNuevaHabitacionClicked).grid(row=0, column=0, padx=5)
        ttk.Button(self.botones_frame, text="Editar").grid(row=0, column=1, padx=5)

    def BtnSearchClicked(self):
        try:
            self.habitacion = buscar_habitacion(self.data, self.numero_busqueda.get())
            if(self.habitacion):
                self.habitacion_id_entry.delete(0, tk.END)
                self.habitacion_id_entry.insert(0, str(self.habitacion.id))
                self.numero_entry.delete(0, tk.END)
                self.numero_entry.insert(0, self.habitacion.numero_habitacion)
                self.estado_combobox.set(self.habitacion.estado)
            else:
                messagebox.showerror("Error", f"No se encontro la habitacion: {self.numero_busqueda.get()}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def BtnNuevaHabitacionClicked(self):
        try:
            nueva_habitacion = Habitacion(int(self.habitacion_id_entry.get()), self.numero_entry.get(), self.estado_combobox.get())
            agregar_habitacino(self.data, nueva_habitacion)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

