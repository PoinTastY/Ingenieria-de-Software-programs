class Cliente:
    def __init__(self, id: int = 0, nombre: str = "", apellido: str = "", telefono: str = "", puntos: int = 0, direccion: str = "", email: str = ""):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.puntos = puntos
        self.direccion = direccion
        self.email = email

    def __repr__(self):
        return (f"Cliente(id={self.id}, nombre='{self.nombre}', apellido='{self.apellido}', "
                f"direccion='{self.direccion}', email='{self.email}', telefono='{self.telefono}', "
                f"puntos={self.puntos})")