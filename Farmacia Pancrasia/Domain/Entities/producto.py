class Producto:
    def __init__(self, id : int, codigo : str, descripcion : str, precio : float, stock : float):
        self.id = id
        self.codigo = codigo
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock