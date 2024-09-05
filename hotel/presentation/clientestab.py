from tkinter import ttk

class ClientesTab(ttk.Frame):
    def __init__(self, parent, data):
        super().__init__(parent)

        self.data = data

        # Labels y Entradas para buscar y detalles del cliente
        ttk.Label(self, text="Ingrese Id del Cliente:").grid(row=0, column=0, padx=5, pady=5)
        self.id_busqueda = ttk.Entry(self)
        self.id_busqueda.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self, text="Buscar").grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(self, text="ID:").grid(row=1, column=0, padx=5, pady=5)
        self.id_entry = ttk.Entry(self)
        self.id_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="Nombre:").grid(row=2, column=0, padx=5, pady=5)
        self.nombre_entry = ttk.Entry(self)
        self.nombre_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text="Direccion:").grid(row=3, column=0, padx=5, pady=5)
        self.direccion_entry = ttk.Entry(self)
        self.direccion_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self, text="Telefono:").grid(row=4, column=0, padx=5, pady=5)
        self.telefono_entry = ttk.Entry(self)
        self.telefono_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self, text="Email:").grid(row=5, column=0, padx=5, pady=5)
        self.email_entry = ttk.Entry(self)
        self.email_entry.grid(row=5, column=1, padx=5, pady=5)

        # Botones de control
        self.botones_frame = ttk.Frame(self)
        self.botones_frame.grid(row=6, column=0, columnspan=3, pady=10)

        ttk.Button(self.botones_frame, text="Nuevo").grid(row=0, column=0, padx=5)
        ttk.Button(self.botones_frame, text="Salvar").grid(row=0, column=1, padx=5)
        ttk.Button(self.botones_frame, text="Cancelar").grid(row=0, column=2, padx=5)
        ttk.Button(self.botones_frame, text="Editar").grid(row=0, column=3, padx=5)
        ttk.Button(self.botones_frame, text="Eliminar").grid(row=0, column=4, padx=5)