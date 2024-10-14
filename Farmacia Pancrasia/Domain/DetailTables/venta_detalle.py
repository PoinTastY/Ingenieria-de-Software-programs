class VentaDetalle:
    def __init__(self, id : int, id_venta : int, id_producto : int, cantidad : float):
        self.id = id
        self.id_venta = id_venta
        self.id_producto = id_producto
        self.cantidad = cantidad