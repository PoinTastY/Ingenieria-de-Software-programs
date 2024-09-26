import tkinter as tk
<<<<<<< HEAD
from tkinter import ttk, messagebox

from Data.db_repo import DBRepo

class Clientes(tk.Tk):
    def __init__(self, db_repo : DBRepo, main_page):
        super().__init__()
        self.db_repo = db_repo
        self.mainwindow = main_page
        self.title("Clientes")
        self.geometry("450x400")
        
    def build_ui(self):
        tk.Label(self, text="Ingrese id a buscar:").grid(row=0, column=0, padx=10, pady=10)
        entry_buscar_id = tk.Entry(self)
        entry_buscar_id.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self, text="Search", command=lambda: self.buscar_cliente(entry_buscar_id.get())).grid(row=0, column=2, padx=10, pady=10)

        tk.Label(self, text="ID:").grid(row=1, column=0, padx=10, pady=10)
        entry_id_cliente = tk.Entry(self)
        entry_id_cliente.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self, text="User Name:").grid(row=2, column=0, padx=10, pady=10)
        entry_nombre_usuario = tk.Entry(self)
        entry_nombre_usuario.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self, text="Customer Name:").grid(row=3, column=0, padx=10, pady=10)
        entry_nombre_cliente = tk.Entry(self)
        entry_nombre_cliente.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(self, text="Phone:").grid(row=4, column=0, padx=10, pady=10)
        entry_telefono = tk.Entry(self)
        entry_telefono.grid(row=4, column=1, padx=10, pady=10)

        btn_nuevo = tk.Button(self, text="New", command=lambda: self.limpiar_campos(entry_id_cliente, entry_nombre_usuario, entry_nombre_cliente, entry_telefono))
        btn_nuevo.grid(row=5, column=0, padx=10, pady=10)

        btn_guardar = tk.Button(self, text="Save", command=lambda: self.guardar_cliente(entry_id_cliente.get(), entry_nombre_usuario.get(), entry_nombre_cliente.get(), entry_telefono.get()))
        btn_guardar.grid(row=5, column=1, padx=10, pady=10)

        btn_cancelar = tk.Button(self, text="Cancel", command=self.cancelar)
        btn_cancelar.grid(row=5, column=2, padx=10, pady=10)

        btn_editar = tk.Button(self, text="Edit")
        btn_editar.grid(row=5, column=3, padx=10, pady=10)

    def cancelar(self):
        self.destroy()
        self.mainwindow.deiconify()
    
    def limpiar_campos(self, *campos):
        for campo in campos:
            campo.delete(0, tk.END)

    def buscar_cliente(self, id_cliente):
        pass

    def guardar_cliente(self, id_cliente, nombre_usuario, nombre_cliente, telefono):
        

