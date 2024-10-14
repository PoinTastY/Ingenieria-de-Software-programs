import psycopg2

from Domain.Entities.usuario import Usuario


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
    
    def __del__(self):
        self.cursor.close()
        self.conn.close()