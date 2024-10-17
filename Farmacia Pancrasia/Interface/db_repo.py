import psycopg2

from Domain.Entities.usuario import Usuario
from Domain.Entities.producto import Producto


class DbRepo:
    def __init__(self):
        self.conn = psycopg2.connect(database = "pdv",
                                    user = "admin",
                                    host= 'localhost',
                                    password = "staremedic1",
                                    port = 5432)
        
        self.cursor = self.conn.cursor()

    def login(self, user : str, password : str):
        self.cursor.execute("SELECT * FROM usuario WHERE nombre = %s AND password = %s", (user, password))
        user = self.cursor.fetchone()
        if user:
            return Usuario(user[0], user[1], user[2], user[3])
        return None
    
    def create_producto(self, codigo : str, descripcion : str, precio : float, stock : float):
        #first validate if the product exists
        self.cursor.execute("SELECT * FROM producto WHERE codigo = %s", (codigo,))
        product = self.cursor.fetchone()
        if product:
            self.update_producto(codigo, descripcion, precio, stock)
            return
        self.cursor.execute("INSERT INTO producto (codigo, descripcion, precio, stock) VALUES (%s, %s, %s, %s)", (codigo, descripcion, precio, stock))
        self.conn.commit()

    def update_producto(self, codigo : str, descripcion : str, precio : float, stock : float):
        self.cursor.execute("UPDATE producto SET descripcion = %s, precio = %s, stock = %s WHERE codigo = %s", (descripcion, precio, stock, codigo))
        self.conn.commit()

    def search_producto(self, codigo : str):
        self.cursor.execute("SELECT * FROM producto WHERE codigo = %s", (codigo,))
        product = self.cursor.fetchone()
        if product:
            #create a Producto object
            return Producto(id=product[0], codigo=product[1], descripcion=product[2], precio=product[3], stock=product[4])
        return None

    def buscar_usuario(self, nombre : str):
        self.cursor.execute("SELECT * FROM usuario WHERE nombre = %s", (nombre,))
        user = self.cursor.fetchone()
        if user:
            return Usuario(id=user[0], nombre=user[1], password=user[2], perfil=user[3])
        return None
    
    def create_usuario(self, nombre : str, password : str, perfil : str):
        #first validate if the user exists
        user = self.buscar_usuario(nombre)
        if user is not None:
            self.update_usuario(nombre, password, perfil)
            return
        
        self.cursor.execute("INSERT INTO usuario (nombre, password, perfil) VALUES (%s, %s, %s)", (nombre, password, perfil))
        self.conn.commit()

    def delete_usuario(self, nombre : str):
        if(nombre == "admin"):
            raise Exception("No se puede eliminar el usuario admin, solo editar su contraseña")
        self.cursor.execute("DELETE FROM usuario WHERE nombre = %s", (nombre,))
        self.conn.commit()

    def obtener_siguiente_id_usuario(self):
        self.cursor.execute("SELECT MAX(id) FROM usuario")
        id = self.cursor.fetchone()
        if id:
            return id[0] + 1
        return 1

    def update_usuario(self, nombre : str, password : str, perfil : str):
        if(nombre == "admin"):
            self.cursor.execute("UPDATE usuario SET password = %s WHERE nombre = %s", (password, nombre))
            self.conn.commit()
            return
        self.cursor.execute("UPDATE usuario SET password = %s, perfil = %s WHERE nombre = %s", (password, perfil, nombre))
        self.conn.commit()

    def read_producto(self, codigo : str):
        self.cursor.execute("SELECT * FROM producto WHERE codigo = %s", (codigo,))
        product = self.cursor.fetchone()
        if product:
            return product
        return None

    
    def __del__(self):
        self.cursor.close()
        self.conn.close()