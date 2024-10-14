import tkinter as tk

class VentaTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack()
        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="Venta").pack(padx=10, pady=5)
        tk.Label(self, text="Cliente:").pack(padx=10, pady=5)
        self.entry_cliente = tk.Entry(self)
