class CompraDetalle:
    def __init__(self, id : int, id_compra : int, id_producto : int, cantidad : float):
        self.id = id
        self.id_compra = id_compra
        self.id_producto = id_producto
        self.cantidad = cantidad