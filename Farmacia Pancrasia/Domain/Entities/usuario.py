class Usuario:
    def __init__(self, id : int, nombre : str, password : str, perfil : str):
        self.id = id
        self.nombre = nombre
        self.password = password
        self.perfil = perfil

    def __repr__(self):
        return f"Usuario(id={self.id}, nombre='{self.nombre}', password ='{self.password};, perfil='{self.perfil}')"