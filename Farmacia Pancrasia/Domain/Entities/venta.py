import datetime

class Venta:
    def __init__(self, id : int, id_cliente : int, id_usuario : int, fecha : datetime, total : float):
        self.id = id
        self.id_cliente = id_cliente
        self.id_usuario = id_usuario
        self.fecha = fecha
        self.total = total