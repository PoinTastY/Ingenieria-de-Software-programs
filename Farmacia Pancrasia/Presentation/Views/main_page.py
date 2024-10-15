from tkinter import messagebox, ttk
import tkinter as tk

from Interface.db_repo import DbRepo
from Domain.Entities.usuario import Usuario
from Presentation.Views.tabs.venta_tab import VentaTab


class MainPage(tk.Tk):
    def __init__(self, db_repo : DbRepo, user : Usuario, login):
        super().__init__()
        self.db_repo = db_repo
        self.user = user
        self.title("Taller Mecanico")
        self.geometry("300x300")
        self.login = login
        self.build_ui()

    def build_ui(self):
        self.notebook = ttk.Notebook(self)

        #define tabs
        self.ventas_tab = VentaTab(self.notebook, self.db_repo)

        #add tabs
        self.notebook.add(self.ventas_tab, text="Ventas")

        #finally pack  the notebook
        self.notebook.pack(fill="both", expand=True)
