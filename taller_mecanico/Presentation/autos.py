from tkinter import messagebox
import tkinter as tk

from Data.db_repo import DBRepo

import tkinter as tk
from tkinter import messagebox

class Autos(tk.Tk):
    def __init__(self, db_repo: DBRepo, main_page, user):
        super().__init__()
        self.db_repo = db_repo
        self.mainwindow = main_page
        self.user = user
        self.title("Autos")
        self.geometry("550x300")
        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="Ingrese ID del vehículo a buscar:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_buscar_id = tk.Entry(self)
        self.entry_buscar_id.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self, text="Buscar", command=lambda: self.buscar_auto(self.entry_buscar_id.get())).grid(row=0, column=2, padx=10, pady=10)

        tk.Label(self, text="ID Vehículo:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_id_auto = tk.Entry(self, state=tk.DISABLED)
        self.entry_id_auto.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self, text="ID Cliente:").grid(row=2, column=0, padx=10, pady=10)
        self.entry_id_cliente = tk.Entry(self, state=tk.DISABLED)
        self.entry_id_cliente.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self, text="Marca:").grid(row=3, column=0, padx=10, pady=10)
        self.entry_marca = tk.Entry(self, state=tk.DISABLED)
        self.entry_marca.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(self, text="Modelo:").grid(row=4, column=0, padx=10, pady=10)
        self.entry_modelo = tk.Entry(self, state=tk.DISABLED)
        self.entry_modelo.grid(row=4, column=1, padx=10, pady=10)

        tk.Label(self, text="Año:").grid(row=5, column=0, padx=10, pady=10)
        self.entry_año = tk.Entry(self, state=tk.DISABLED)
        self.entry_año.grid(row=5, column=1, padx=10, pady=10)

        self.btn_nuevo = tk.Button(self, text="Nuevo", command=self.nuevo_auto)
        self.btn_nuevo.grid(row=6, column=0, padx=10, pady=10)

        self.btn_guardar = tk.Button(self, text="Guardar", state=tk.DISABLED, command=lambda: self.guardar_auto(id_vehiculo=self.entry_id_auto.get(), 
                                                                                                                id_cliente=self.entry_id_cliente.get(), marca=self.entry_marca.get(),
                                                                                                                modelo=self.entry_modelo.get(), anio=self.entry_año.get()))
        self.btn_guardar.grid(row=6, column=1, padx=10, pady=10)

        self.btn_cancelar = tk.Button(self, text="Cancelar", command=self.cancelar)
        self.btn_cancelar.grid(row=6, column=2, padx=10, pady=10)

        self.btn_editar = tk.Button(self, state=tk.DISABLED, text="Editar", command=self.editar_auto)
        self.btn_editar.grid(row=6, column=3, padx=10, pady=10)

        self.btn_eliminar = tk.Button(self, state=tk.DISABLED, text="Eliminar", command=self.eliminar_auto)
        self.btn_eliminar.grid(row=6, column=4, padx=10, pady=10)

    def cancelar(self):
        self.destroy()
        self.mainwindow.deiconify()

    def limpiar_campos(self, *campos):
        for campo in campos:
            campo.delete(0, tk.END)

    def habilitar_deshabilitar_campos(self, *campos, state):
        for campo in campos:
            campo.config(state=state)

    def buscar_auto(self, id_vehiculo):
        try:
            id_vehiculo = id_vehiculo.upper()
            auto = self.db_repo.buscar_auto(id_vehiculo)
            if auto:
                self.habilitar_deshabilitar_campos(self.entry_id_auto, self.entry_id_cliente,
                                                    self.entry_marca, self.entry_modelo, self.entry_año, self.btn_editar, state=tk.NORMAL)
                self.entry_id_auto.insert(0, auto.id_vehiculo)
                self.entry_id_cliente.insert(0, auto.id_cliente)
                self.entry_marca.insert(0, auto.marca)
                self.entry_modelo.insert(0, auto.modelo)
                self.entry_año.insert(0, auto.anio)

                self.habilitar_deshabilitar_campos(self.entry_id_auto, state=tk.DISABLED)
                self.habilitar_deshabilitar_campos(self.btn_eliminar, state=tk.NORMAL)
            else:
                messagebox.showerror("Error", "Vehículo no encontrado")
        except Exception as e:
            messagebox.showerror("Error", "Error al buscar vehículo. ({})".format(e))

    def eliminar_auto(self):
        try:
            self.db_repo.borrar_auto(self.entry_id_auto.get())
            messagebox.showinfo("Vehículo eliminado", "Vehículo eliminado correctamente")
            self.limpiar_campos(self.entry_id_auto, self.entry_id_cliente, self.entry_marca, self.entry_modelo, self.entry_año)
            self.habilitar_deshabilitar_campos(self.entry_id_auto, self.entry_id_cliente, self.entry_marca, self.entry_modelo, self.entry_año, self.btn_editar, self.btn_eliminar, state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", "Error al eliminar vehículo. ({})".format(e))

    def editar_auto(self):
        self.habilitar_deshabilitar_campos(self.entry_id_cliente, self.entry_marca, self.entry_modelo, self.entry_año, self.btn_guardar, self.btn_eliminar, state=tk.NORMAL)
        self.habilitar_deshabilitar_campos(self.btn_nuevo, self.entry_id_auto, state=tk.DISABLED)

    def nuevo_auto(self):
        self.habilitar_deshabilitar_campos(self.entry_id_auto, self.entry_id_cliente, self.entry_marca, self.entry_modelo, self.entry_año, self.btn_guardar, state=tk.NORMAL)
        self.habilitar_deshabilitar_campos(self.btn_nuevo, self.btn_eliminar, state=tk.DISABLED)

    def guardar_auto(self, id_vehiculo, id_cliente, marca, modelo, anio):
        try:
            # validar si año es un número
            try:
                int(anio)  # Puedes validar el formato de año según tu requerimiento
            except:
                messagebox.showerror("Error", "El año debe ser un número")
                return
            id_vehiculo = id_vehiculo.upper()
            self.db_repo.guardar_auto(placa=id_vehiculo, id_cliente=id_cliente, marca=marca, modelo=modelo, anio=anio)
            messagebox.showinfo("Vehículo guardado", "Vehículo guardado correctamente")
            self.habilitar_deshabilitar_campos(self.btn_nuevo, self.entry_id_auto, state=tk.NORMAL)
            self.limpiar_campos(self.entry_id_auto, self.entry_id_cliente, self.entry_marca, self.entry_modelo, self.entry_año)
            self.habilitar_deshabilitar_campos(self.entry_id_auto, self.entry_id_cliente, self.entry_marca, self.entry_modelo, self.entry_año, self.btn_guardar, state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", "Error al guardar vehículo. ({})".format(e))
