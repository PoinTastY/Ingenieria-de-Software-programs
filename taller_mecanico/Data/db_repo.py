import psycopg2

conn = psycopg2.connect(database = "taller_mecanico", 
                        user = "admin", 
                        host= 'localhost',
                        password = "csisgod69",
                        port = 5432)