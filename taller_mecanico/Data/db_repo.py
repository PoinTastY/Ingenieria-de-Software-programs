import psycopg2

from Domain.Entities.usuario import Usuario
from Domain.Entities.cliente import Cliente
from Domain.Entities.reparacion import Reparacion
from Domain.Entities.parte import Parte
from Domain.Entities.auto import Auto

class DBRepo:
    def __init__(self):
        self.conn = psycopg2.connect(database = "taller_mecanico",
                                    user = "postgres",
                                    host= 'localhost',
                                    password = "Isee420.69&hear",
                                    port = 5432)
        
        self.cursor = self.conn.cursor()

    def obtener_siguiente_id_usuario(self) -> int:
        try:
            self.cursor.execute("SELECT MAX(id) FROM usuarios")
            id = self.cursor.fetchone()[0]
            return id + 1
        except Exception as e:
            raise e


    def buscar_usuario(self, id_usuario) -> Usuario:
        try:
            self.cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id_usuario,))
            user = self.cursor.fetchone()
            if user:
                user = Usuario(id=user[0], nombre=user[1], password=user[2], perfil=user[3])
                return user
            else:
                return None
        except Exception as e:
            raise e


    def guardar_usuario(self, id_usuario : str, nombre : str, password : str, perfil : str) -> None:
        try:
            #validate if user exists, if so, edit it instead of creating a new one
            if(self.buscar_usuario(id_usuario)):
                self.editar_usuario(id_usuario, nombre, password, perfil)
                return
            self.cursor.execute("INSERT INTO usuarios (nombre, password, perfil) VALUES (%s, %s, %s)", (nombre, password, perfil))
            self.conn.commit()
        except Exception as e:
            raise e
        
    def editar_usuario(self, id_usuario : int, nombre : str, password : str, perfil : str) -> None:
        try:
            self.cursor.execute("UPDATE usuarios SET nombre = %s, password = %s, perfil = %s WHERE id = %s", (nombre, password, perfil, id_usuario))
            self.conn.commit()
        except Exception as e:
            raise e
        
    def obtener_siguiente_id_clientes(self) -> int:
        try:
            self.cursor.execute("SELECT MAX(id) FROM clientes")

            id = self.cursor.fetchone()[0]
            if(id == None):
                return 1
            return id + 1
        except Exception as e:
            raise e
        
    def buscar_cliente(self, id_cliente) -> Cliente:
        try:
            self.cursor.execute("SELECT * FROM clientes WHERE id = %s", (id_cliente,))
            cliente = self.cursor.fetchone()
            if cliente:
                cliente = Cliente(id=cliente[0], nombre=cliente[1], apellido=cliente[2], telefono=cliente[3])
                return cliente
            else:
                return None
        except Exception as e:
            raise e
        
    def guardar_cliente(self,id : int, nombre : str, apellido : str, telefono : str) -> None:
        try:
            if(self.buscar_cliente(id)):
                self.editar_cliente(id, nombre, apellido, telefono)
                return
            self.cursor.execute("INSERT INTO clientes (nombre, apellido, telefono) VALUES (%s, %s, %s)", (nombre, apellido, telefono))
            self.conn.commit()
        except Exception as e:
            raise e
        
    def borrar_cliente(self, id_cliente : int) -> None:
        try:
            cliente_to_delete = self.buscar_cliente(id_cliente)
            if(cliente_to_delete != None):
                self.cursor.execute("DELETE FROM clientes WHERE id = %s", (id_cliente))
                self.conn.commit()
            else:
                raise Exception("Parece que el cliente a eliminar no se encontro en la db")
        except:
            raise
        
    def editar_cliente(self, id_cliente : int, nombre : str, apellido : str,  telefono : str) -> None:
        try:
            self.cursor.execute("UPDATE clientes SET nombre = %s, apellido = %s, telefono = %s WHERE id = %s", (nombre, apellido, telefono, id_cliente))
            self.conn.commit()
        except:
            raise
    
    def login(self, usuario, contraseña) -> Usuario:
        self.cursor.execute("SELECT * FROM usuarios WHERE nombre = %s AND password = %s", (usuario, contraseña))
        user = self.cursor.fetchone()
        if user:
            user = Usuario(id=user[0], nombre=user[1], password=user[2], perfil=user[3])
            return user
        else:
            raise Exception("Usuario o contraseña incorrecta")
            
    
    def borrar_usuario(self, id_usuario : int) -> None:
        try:
            user_to_delete = self.buscar_usuario(id_usuario)
            if(user_to_delete != None):
                self.cursor.execute("DELETE FROM usuarios WHERE id = %s", (id_usuario))
                self.conn.commit()
            else:
                raise Exception("Parece que el usuario a eliminar no se encontro en la db")
        except:
            raise


    def guardar_auto(self, placa: str, id_cliente: int, marca: str, modelo: str, anio: str) -> None:
        try:
            # Verificar si el cliente existe en la base de datos
            if not self.buscar_cliente(id_cliente):
                raise Exception("El cliente no existe en la db")

            # Si el auto ya existe, editarlo en lugar de insertar uno nuevo
            if self.buscar_auto(placa):
                self.editar_auto(placa, id_cliente, marca, modelo, anio)
            else:
                # Insertar todos los campos en la base de datos
                self.cursor.execute(
                    "INSERT INTO vehiculos (id_vehiculo, id_cliente, marca, modelo, anio) VALUES (%s, %s, %s, %s, %s)",
                    (placa, id_cliente, marca, modelo, anio)
                )
                self.conn.commit()
        except Exception as e:
            raise e

    def editar_auto(self, placa: str, id_cliente: int, marca: str, modelo: str, anio: str) -> None:
        try:
            # Actualizar todos los campos del vehículo en la base de datos
            self.cursor.execute(
                """
                UPDATE vehiculos
                SET id_cliente = %s, marca = %s, modelo = %s, anio = %s
                WHERE id_vehiculo = %s
                """,
                (id_cliente, marca, modelo, anio, placa)
            )
            self.conn.commit()
        except Exception as e:
            raise e

    def buscar_auto(self, placa) -> Auto:
        try:
            self.cursor.execute("SELECT * FROM vehiculos WHERE id_vehiculo = %s", (placa,))
            auto = self.cursor.fetchone()
            if auto:
                auto = Auto(id_vehiculo=auto[0], id_cliente=auto[1], marca=auto[2], modelo=auto[3], anio=auto[4])
                return auto
            else:
                return None
        except Exception as e:
            raise e

    def borrar_auto(self, placa) -> None:
        try:
            auto_to_delete = self.buscar_auto(placa)
            if(auto_to_delete != None):
                self.cursor.execute("DELETE FROM vehiculos WHERE id_vehiculo = %s", (placa))
                self.conn.commit()
            else:
                raise Exception("Parece que el auto a eliminar no se encontro en la db")
        except:
            raise

    def obtener_siguiente_id_reparaciones(self) -> int:
        try:
            self.cursor.execute("SELECT MAX(id) FROM reparaciones")
            id = self.cursor.fetchone()[0]
            if(id == None):
                return 1
            return id + 1
        except Exception as e:
            raise e
        
    def buscar_reparacion(self, id_reparacion) -> Reparacion:
        try:
            self.cursor.execute("SELECT * FROM reparaciones WHERE id = %s", (id_reparacion,))
            reparacion = self.cursor.fetchone()
            if reparacion:
                reparacion = Reparacion(id=reparacion[0],  id_vehiculo=reparacion[1], descripcion=reparacion[2], fecha_inicio=reparacion[3], fecha_entrega=reparacion[4], id_mecanico=reparacion[5])
                return reparacion
            else:
                return None
        except Exception as e:
            raise e
        
    def guardar_reparacion(self, id_reparacion, id_vehiculo, descripcion, fecha_inicio, fecha_entrega, id_mecanico) -> None:
        try:
            if(self.buscar_reparacion(id_reparacion)):
                self.editar_reparacion(id_reparacion, id_vehiculo, descripcion, fecha_inicio, fecha_entrega, id_mecanico)
                return
            self.cursor.execute("INSERT INTO reparaciones (id_vehiculo, descripcion, fecha_inicio, fecha_entrega, id_mecanico) VALUES (%s, %s, %s, %s, %s)", (id_vehiculo, descripcion, fecha_inicio, fecha_entrega, id_mecanico))
            self.conn.commit()
        except Exception as e:
            raise e
        
    def editar_reparacion(self, id_reparacion, id_vehiculo, descripcion, fecha_inicio, fecha_entrega, id_mecanico) -> None:
        try:
            self.cursor.execute("UPDATE reparaciones SET id_vehiculo = %s, descripcion = %s, fecha_inicio = %s, fecha_entrega = %s, id_mecanico = %s WHERE id = %s", (id_vehiculo, descripcion, fecha_inicio, fecha_entrega, id_mecanico, id_reparacion))
            self.conn.commit()
        except Exception as e:
            raise e
        
    def borrar_reparacion(self, id_reparacion) -> None:
        try:
            reparacion_to_delete = self.buscar_reparacion(id_reparacion)
            if(reparacion_to_delete != None):
                self.cursor.execute("DELETE FROM reparaciones WHERE id = %s", (id_reparacion))
                self.conn.commit()
            else:
                raise Exception("Parece que la reparacion a eliminar no se encontro en la db")
        except:
            raise

    def obtener_siguiente_id_partes(self) -> int:
        try:
            self.cursor.execute("SELECT MAX(id) FROM partes")
            id = self.cursor.fetchone()[0]
            if(id == None):
                return 1
            return id + 1
        except Exception as e:
            raise e
        
    def buscar_parte(self, id_parte) -> Parte:
        try:
            self.cursor.execute("SELECT * FROM partes WHERE id = %s", (id_parte,))
            parte = self.cursor.fetchone()
            if parte:
                parte = Parte(id=parte[2], nombre=parte[0], costo=parte[1])
                return parte
            else:
                return None
        except Exception as e:
            raise e
        
    def guardar_parte(self, id_parte, nombre, costo) -> None:
        try:
            if(self.buscar_parte(id_parte)):
                self.editar_parte(id_parte, nombre, costo)
                return
            self.cursor.execute("INSERT INTO partes (nombre, costo) VALUES (%s, %s)", (nombre, costo))
            self.conn.commit()
        except Exception as e:
            raise e
        
    def editar_parte(self, id_parte, nombre, costo) -> None:
        try:
            self.cursor.execute("UPDATE partes SET nombre = %s, costo = %s WHERE id = %s", (nombre, costo, id_parte))
            self.conn.commit()
        except Exception as e:
            raise e
        
    def borrar_parte(self, id_parte) -> None:
        try:
            parte_to_delete = self.buscar_parte(id_parte)
            if(parte_to_delete != None):
                self.cursor.execute("DELETE FROM partes WHERE id = %s", (id_parte))
                self.conn.commit()
            else:
                raise Exception("Parece que la parte a eliminar no se encontro en la db")
        except:
            raise
    
    def obtener_nombre_pieza(self, id_pieza) -> str:
        try:
            self.cursor.execute("SELECT nombre FROM partes WHERE id = %s", (id_pieza,))
            nombre = self.cursor.fetchone()[0]
            return nombre
        except Exception as e:
            raise e
        
    def obtener_partes_reparacion(self, id_reparacion) -> list:
        try:
            self.cursor.execute("SELECT * FROM det_rep_parte WHERE id_rep = %s", (id_reparacion,))
            tabla_intermedia = self.cursor.fetchall()
            partes = []
            for parte in tabla_intermedia:
                id = parte[1]
                partes.append(self.buscar_parte(id))

            return partes
        except Exception as e:
            raise e
        
    def obtener_cantidad_parte(self, id_reparacion, id_parte) -> int:
        try:
            self.cursor.execute("SELECT cantidad FROM det_rep_parte WHERE id_rep = %s AND id_pieza = %s", (id_reparacion, id_parte))
            cantidad = self.cursor.fetchone()[0]
            return cantidad
        except Exception as e:
            raise e

    def obtener_costo_pieza(self, id_parte):
        try:
            self.cursor.execute("SELECT costo FROM partes WHERE id = %s", (id_parte))
            costo = self.cursor.fetchone()[0]
            return costo
        except Exception as e:
            raise e
        
    def agregar_det_rep_parte(self, id_reparacion, id_parte, cantidad) -> None:
        try:
            self.cursor.execute("INSERT INTO det_rep_parte (id_rep, id_pieza, cantidad) VALUES (%s, %s, %s)", (id_reparacion, id_parte, cantidad))
            self.conn.commit()
        except Exception as e:
            raise e
        
    def eliminar_det_rep_parte(self, id_reparacion, id_parte) -> None:
        try:
            self.cursor.execute("DELETE FROM det_rep_parte WHERE id_rep = %s AND id_pieza = %s", (id_reparacion, id_parte))
            self.conn.commit()
        except Exception as e:
            raise e

        
    def __del__(self):
        self.cursor.close()
        self.conn.close()