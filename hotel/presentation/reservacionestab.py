from tkinter import ttk

class ReservacionesTab(ttk.Frame):
    def __init__(self, parent, data):
        super().__init__(parent)

        self.data = data

        # Labels y Entradas para buscar y detalles de la reservación
        ttk.Label(self, text="Ingrese Reservación:").grid(row=0, column=0, padx=5, pady=5)
        self.reservacion_busqueda = ttk.Entry(self)
        self.reservacion_busqueda.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self, text="Buscar Reservacion").grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(self, text="Reservacion ID:").grid(row=1, column=0, padx=5, pady=5)
        self.reservacion_id_entry = ttk.Entry(self)
        self.reservacion_id_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="Cliente ID:").grid(row=2, column=0, padx=5, pady=5)
        self.cliente_id_entry = ttk.Combobox(self, values=["1", "2", "3"])
        self.cliente_id_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text="Habitacion ID:").grid(row=3, column=0, padx=5, pady=5)
        self.habitacion_id_entry = ttk.Combobox(self, values=["10", "11", "12"])
        self.habitacion_id_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self, text="Fecha Reservacion:").grid(row=4, column=0, padx=5, pady=5)
        self.fecha_reservacion_entry = ttk.Entry(self)
        self.fecha_reservacion_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self, text="Fecha Salida:").grid(row=5, column=0, padx=5, pady=5)
        self.fecha_salida_entry = ttk.Entry(self)
        self.fecha_salida_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(self, text="Hora Reservacion:").grid(row=6, column=0, padx=5, pady=5)
        self.hora_reservacion_entry = ttk.Entry(self)
        self.hora_reservacion_entry.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(self, text="Costo:").grid(row=7, column=0, padx=5, pady=5)
        self.costo_entry = ttk.Entry(self)
        self.costo_entry.grid(row=7, column=1, padx=5, pady=5)

        # Botones de control
        self.botones_frame = ttk.Frame(self)
        self.botones_frame.grid(row=8, column=0, columnspan=3, pady=10)

        ttk.Button(self.botones_frame, text="Nueva Reservacion").grid(row=0, column=0, padx=5)
        ttk.Button(self.botones_frame, text="Reservar").grid(row=0, column=1, padx=5)
        ttk.Button(self.botones_frame, text="Cancelar Reservacion").grid(row=0, column=2, padx=5)
        ttk.Button(self.botones_frame, text="Editar").grid(row=0, column=3, padx=5)