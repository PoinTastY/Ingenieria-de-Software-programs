class Habitacion:
    def __init__(self, id : int,  numero_habitacion, estado : str) -> None:
        self.id = int(id)
        self.numero_habitacion = numero_habitacion
        self.estado = estado

    def GetId(self) -> int:
        return self.id
    
    def GetNumeroHabitacion(self) -> str:
        return self.numero_habitacion
    
    def GetEstado(self) -> str:
        return self.estado