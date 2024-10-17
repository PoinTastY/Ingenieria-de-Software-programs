from tkinter import messagebox, ttk
import tkinter as tk

from Interface.db_repo import DbRepo
from Domain.Entities.usuario import Usuario
from Presentation.Views.tabs.venta_tab import VentaTab
from Presentation.Views.tabs.add_producto_tab import AddProductoTab
from Presentation.Views.tabs.usuarios_tab import UsuariosTab


class MainPage(tk.Tk):
    def __init__(self, db_repo : DbRepo, user : Usuario, login):
        super().__init__()
        self.db_repo = db_repo
        self.user = user
        self.title("Taller Mecanico")
        self.geometry("670x500")
        self.login = login
        self.build_ui()

    def build_ui(self):
        self.notebook = ttk.Notebook(self)

        #define tabs
        self.ventas_tab = VentaTab(self.notebook, self.db_repo)
        self.add_producto_tab = AddProductoTab(self.notebook, self.db_repo)
        self.usuarios_tab = UsuariosTab(self.notebook, self.db_repo)

        #add tabs
        self.notebook.add(self.ventas_tab, text="Ventas")
        self.notebook.add(self.add_producto_tab, text="Productos")
        self.notebook.add(self.usuarios_tab, text="Usuarios")

        #finally pack  the notebook
        self.notebook.pack(fill="both", expand=True)

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        self.bind("<Return>", self.on_enter_pressed)


    def on_enter_pressed(self, event):
        selected_tab = self.notebook.select()
        frame = self.notebook.nametowidget(selected_tab)
        if frame == self.add_producto_tab:
            self.add_producto_tab.buscar_producto(event)
        if frame == self.ventas_tab:
            self.ventas_tab.buscar_producto(event)

    def on_tab_change(self, event):
        selected_tab = self.notebook.select()
        frame = self.notebook.nametowidget(selected_tab)
        if frame == self.add_producto_tab:
            self.add_producto_tab.clear_inputs()
            self.add_producto_tab.entry_codigo.delete(0, tk.END)
            self.add_producto_tab.entry_codigo.focus_set()

        if frame == self.ventas_tab:
            self.ventas_tab.entry_codigo.delete(0, tk.END)
            self.ventas_tab.entry_codigo.focus_set()
        
        if frame == self.usuarios_tab:
            self.usuarios_tab.clear_inputs()
            

