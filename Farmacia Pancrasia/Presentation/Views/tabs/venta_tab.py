import tkinter as tk

from Interface.db_repo import DbRepo

class VentaTab(tk.Frame):
    def __init__(self, parent, db_repo : DbRepo):
        super().__init__(parent)
        self.parent = parent
        self.db_repo = db_repo
        self.pack()
        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="Venta").pack(padx=10, pady=5)
        tk.Label(self, text="Cliente:").pack(padx=10, pady=5)
        self.entry_cliente = tk.Entry(self)
