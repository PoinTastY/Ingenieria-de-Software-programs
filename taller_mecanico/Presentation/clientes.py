import tkinter as tk
from tkinter import ttk, messagebox

from Data.db_repo import DBRepo

class Clientes(tk.Tk):
    def __init__(self, db_repo : DBRepo, main_page, user):
        super().__init__()
        self.db_repo = db_repo
        self.mainwindow = main_page
        self.user = user
        self.title("Clientes")
        self.geometry("450x400")
        self.build_ui()
        
    def build_ui(self):
        tk.Label(self, text="Ingrese id a buscar:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_buscar_id = tk.Entry(self)
        self.entry_buscar_id.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self, text="Search", command=lambda: self.buscar_cliente(self.entry_buscar_id.get())).grid(row=0, column=2, padx=10, pady=10)

        tk.Label(self, text="ID:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_id_cliente = tk.Entry(self, state=tk.DISABLED)
        self.entry_id_cliente.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self, text="Nombre de cliente:").grid(row=2, column=0, padx=10, pady=10)
        self.entry_nombre_usuario = tk.Entry(self, state=tk.DISABLED)
        self.entry_nombre_usuario.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self, text="Apellido de cliente:").grid(row=3, column=0, padx=10, pady=10)
        self.entry_nombre_cliente = tk.Entry(self, state=tk.DISABLED)
        self.entry_nombre_cliente.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(self, text="Telefono:").grid(row=4, column=0, padx=10, pady=10)
        self.entry_telefono = tk.Entry(self, state=tk.DISABLED)
        self.entry_telefono.grid(row=4, column=1, padx=10, pady=10)

        self.btn_nuevo = tk.Button(self, text="New", state=tk.NORMAL, command=self.nuevo_cliente)
        self.btn_nuevo.grid(row=5, column=0, padx=10, pady=10)

        self.btn_guardar = tk.Button(self, text="Save", state=tk.DISABLED, command=lambda: self.guardar_cliente( self.entry_id_cliente.get(), self.entry_nombre_usuario.get(), self.entry_nombre_cliente.get(), self.entry_telefono.get()))
        self.btn_guardar.grid(row=5, column=1, padx=10, pady=10)

        self.btn_cancelar = tk.Button(self, text="Cancel", command=self.cancelar)
        self.btn_cancelar.grid(row=5, column=2, padx=10, pady=10)

        self.btn_editar = tk.Button(self, state=tk.DISABLED, text="Edit")
        self.btn_editar.grid(row=5, column=3, padx=10, pady=10)

    def cancelar(self):
        self.destroy()
        self.mainwindow.deiconify()
    
    def limpiar_campos(self, *campos):
        for campo in campos:
            campo.delete(0, tk.END)

    def habilitar_deshabilitar_campos(self, *campos, state):
        for campo in campos:
            campo.config(state=state)

    def buscar_cliente(self, id_cliente):
        try:
            cliente = self.db_repo.buscar_cliente(id_cliente)
            if cliente:
                self.habilitar_deshabilitar_campos(self.entry_id_cliente, self.entry_nombre_usuario,
                                                                              self.entry_nombre_cliente, self.entry_telefono, self.btn_editar, state=tk.NORMAL )
                self.entry_id_cliente.insert(0, cliente.id)
                self.entry_nombre_usuario.insert(0, cliente.nombre_usuario)
                self.entry_nombre_cliente.insert(0, cliente.nombre_cliente)
                self.entry_telefono.insert(0, cliente.telefono)

                self.habilitar_deshabilitar_campos(self.entry_id_cliente, self.entry_nombre_usuario,
                                                                              self.entry_nombre_cliente, self.entry_telefono, state=tk.DISABLED)
                
        except Exception as e:
            messagebox.showerror("Error", "Error al buscar cliente. ({})".format(e))

    def nuevo_cliente(self):
        self.habilitar_deshabilitar_campos(self.entry_id_cliente, self.entry_nombre_usuario,
                                                                              self.entry_nombre_cliente, self.entry_telefono, self.btn_guardar, state=tk.NORMAL )
        self.entry_id_cliente.delete(0, tk.END)
        self.entry_id_cliente.insert(0, self.db_repo.obtener_siguiente_id_clientes())
        self.habilitar_deshabilitar_campos(self.btn_nuevo, state=tk.DISABLED)

    def guardar_cliente(self,id, nombre, apellido, telefono):
        try:
            self.db_repo.guardar_cliente(id, nombre, apellido, telefono)

        except Exception as e:
            messagebox.showerror("Error", "Error al guardar cliente. ({})".format(e))
        

