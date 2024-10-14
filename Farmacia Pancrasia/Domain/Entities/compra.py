import datetime

class Compra:
    def __init__(self, id : int, referencia : str, id_proveedor : int, id_usuario : int, fecha : datetime):
        self.id = id
        self.referencia = referencia
        self.id_proveedor = id_proveedor
        self.id_usuario = id_usuario
        self.fecha = fecha