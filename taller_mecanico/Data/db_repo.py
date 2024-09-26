import psycopg2

from Domain.Entities.usuario import Usuario
from Domain.Entities.cliente import Cliente

class DBRepo:
    def __init__(self):
        self.conn = psycopg2.connect(database = "taller_mecanico",
                                    user = "admin",
                                    host= 'localhost',
                                    password = "csisgod69",
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
                cliente = Cliente(id=cliente[0], nombre=cliente[1], telefono=cliente[2])
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
        
    def editar_cliente(self, id_cliente : int, nombre : str, apellido : str,  telefono : str) -> None:
        try:
            self.cursor.execute("UPDATE clientes SET nombre = %s, apellido = %s, telefono = %s WHERE id = %s", (nombre, apellido, telefono, id_cliente))
            self.conn.commit()
        except Exception as e:
            raise e
    
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
        
    
    def __del__(self):
        self.cursor.close()
        self.conn.close()