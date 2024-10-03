class Reparacion:
    def __init__(self, id, fecha_inicio, fecha_entrega, descripcion, id_vehiculo, id_mecanico):
        self.id = id
        self.id_vehiculo = id_vehiculo
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_entrega = fecha_entrega
        self.id_mecanico = id_mecanico