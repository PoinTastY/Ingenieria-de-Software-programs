import psycopg2

from Domain.Entities.usuario import Usuario

class DBRepo:
    def __init__(self):
        self.conn = psycopg2.connect(database = "taller_mecanico",
                                    user = "admin",
                                    host= '192.168.3.138',
                                    password = "csisgod69",
                                    port = 5432)
        
        self.cursor = self.conn.cursor()


    def obtener_siguiente_id(self) -> int:
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
        except Exception as e:
            raise e


    def guardar_usuario(self,  nombre : str, password : str, perfil : str) -> None:
        try:
            self.cursor.execute("INSERT INTO usuarios (nombre, password, perfil) VALUES (%s, %s, %s)", (nombre, password, perfil))
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
            raise Exception("Usuario o contraseña incorrecta")\
    
    
    def __del__(self):
        self.cursor.close()
        self.conn.close()