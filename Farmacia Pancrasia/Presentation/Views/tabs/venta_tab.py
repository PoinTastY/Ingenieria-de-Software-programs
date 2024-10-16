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
        self.label_codigo = tk.Label(self, text="Producto:")
        self.label_codigo.pack(padx=10, pady=5)
        self.entry_codigo = tk.Entry(self)
        self.entry_codigo.pack(padx=10, pady=5)