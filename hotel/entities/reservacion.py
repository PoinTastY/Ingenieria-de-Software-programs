import datetime


class reservacion:
    def __init__(self, id : int, id_cliente : int, id_habitacion : int, fecha_salida : datetime, costo : float) -> None:
        self.id = id
        self.id_cliente = id_cliente
        self.id_habitacion = id_habitacion
        self.fecha_reservacion = datetime.datetime.now().date().strftime("%Y-%m-%d")
        self.hora_reservacion = datetime.datetime.now().time().strftime("%H:%M:%S")
        self.fecha_salida = fecha_salida.date().strftime("%Y-%m-%d")
        self.costo = costo
        