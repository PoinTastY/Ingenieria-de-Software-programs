import datetime
import psycopg2

from Domain.Entities.usuario import Usuario
from Domain.Entities.producto import Producto
from Domain.Entities.cliente import Cliente


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
        self.cursor.execute("SELECT * FROM producto WHERE codigo = %s", (str(codigo),))
        product = self.cursor.fetchone()
        if product:
            #create a Producto object
            return Producto(id=product[0], codigo=product[1], descripcion=product[2], precio=product[3], stock=product[4])
        raise Exception("Producto no encontrado")
    
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
    
    def buscar_producto_por_nombre(self, busqueda):
        clientes = []
        try:
            # Puedes usar una consulta SQL que filtre los clientes por nombre
            consulta = "SELECT id, codigo, descripcion, precio, stock FROM producto WHERE descripcion ILIKE %s"
            self.cursor.execute(consulta, ('%' + busqueda + '%',))
            resultados = self.cursor.fetchall()
            
            for id_producto, codigo, descripcion, precio, stock in resultados:
                cliente = Producto(id=id_producto, codigo=codigo, descripcion=descripcion, precio=precio, stock=stock)
                clientes.append(cliente)
        except (Exception, psycopg2.DatabaseError) as error:
            raise Exception(f"Error buscando cliente por nombre: {error}")
        
        return clientes
    
    def obtener_producto_por_id(self, id_producto):
        try:
            self.cursor.execute("SELECT * FROM producto WHERE id = %s", (id_producto,))
            producto = self.cursor.fetchone()
            if producto:
                return Producto(id=producto[0], codigo=producto[1], descripcion=producto[2], precio=producto[3], stock=producto[4])
            return None
        except (Exception, psycopg2.DatabaseError) as error:
            raise Exception(f"Error obteniendo cliente por ID: {error}")
        
    def obtener_siguiente_id_cliente(self):
        # Obtiene el nombre de la secuencia asociada a la columna 'id' de la tabla 'cliente'
        self.cursor.execute("SELECT pg_get_serial_sequence('cliente', 'id')")
        secuencia = self.cursor.fetchone()[0]

        # Consulta el siguiente valor proyectado de la secuencia
        self.cursor.execute(f"SELECT last_value + 1 FROM {secuencia}")
        siguiente_id = self.cursor.fetchone()[0]
        return siguiente_id
    
    def registrar_cliente(self, id, nombre, apellido, direccion, email, telefono):
        # if the client exists, update it
        self.cursor.execute("SELECT * FROM cliente WHERE id = %s", (id,))
        cliente = self.cursor.fetchone()
        if cliente:
            self.editar_cliente(cliente[0], nombre, apellido, direccion, email, telefono)
            return True
        self.cursor.execute("INSERT INTO cliente ( nombre, apellido, direccion, email, telefono) VALUES (%s, %s, %s, %s, %s)", ( nombre, apellido, direccion, email, telefono))
        self.conn.commit()
        return True

    def editar_cliente(self, id_cliente, nombre, apellido, direccion, email, telefono):
        try:
            self.cursor.execute("UPDATE cliente SET nombre = %s, apellido = %s, direccion = %s, email = %s, telefono = %s WHERE id = %s", (nombre, apellido, direccion, email, telefono, id_cliente))
            self.conn.commit()
            return True;
        except (Exception, psycopg2.DatabaseError) as error:
            raise Exception(f"Error editando cliente: {error}")
        
    def buscar_cliente_por_nombre(self, nombre):
        clientes = []
        try:
            # Puedes usar una consulta SQL que filtre los clientes por nombre
            consulta = "SELECT id, nombre, apellido, puntos, direccion, email, telefono FROM cliente WHERE nombre ILIKE %s"
            self.cursor.execute(consulta, ('%' + nombre + '%',))
            resultados = self.cursor.fetchall()
            
            for id_cliente, nombre, apellido, puntos, direccion, email, telefono in resultados:
                cliente = Cliente(id=id_cliente, nombre=nombre, apellido=apellido, direccion=direccion, email=email, telefono=telefono, puntos=puntos)
                clientes.append(cliente)
        except (Exception, psycopg2.DatabaseError) as error:
            raise Exception(f"Error buscando cliente por nombre: {error}")
        
        return clientes
    
    def update_cliente_points(self, id_cliente, total):
        #for each 100 pesos, the client gets 1 point
        points = total // 100
        self.cursor.execute("UPDATE cliente SET puntos = puntos + %s WHERE id = %s", (points, id_cliente))
        self.conn.commit()

        return points

    def obtener_clientes(self) -> list:
        clientes = []
        try:
            query = "SELECT id, nombre, apellido, direccion, email, telefono, puntos FROM cliente"
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()
            
            # Procesa los resultados y crea objetos Cliente
            for id_cliente, nombre, apellido, direccion, email, telefono, puntos in resultados:
                cliente = Cliente(id=id_cliente, nombre=nombre, apellido=apellido, direccion=direccion, email=email, telefono=telefono, puntos=puntos)
                clientes.append(cliente)

        except (Exception, psycopg2.DatabaseError) as error:
            raise Exception(f"Error obteniendo clientes: {error}")
        
        return clientes
    
    def eliminar_cliente(self, id_cliente):
        try:
            self.cursor.execute("DELETE FROM cliente WHERE id = %s", (id_cliente,))
            self.conn.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            raise Exception(f"Error eliminando cliente: {error}")
        
    def obtener_cliente_por_id(self, id_cliente):
        try:
            self.cursor.execute("SELECT * FROM cliente WHERE id = %s", (id_cliente,))
            cliente = self.cursor.fetchone()
            if cliente:
                return Cliente(id=cliente[0], nombre=cliente[1], apellido=cliente[2], direccion=cliente[3], email=cliente[4], telefono=cliente[5], puntos=cliente[6])
            return None
        except (Exception, psycopg2.DatabaseError) as error:
            raise Exception(f"Error obteniendo cliente por ID: {error}")
        
    def create_venta(self, id_cliente, id_usuario, total) -> int:
        try:
            
            fecha = datetime.datetime.now()
            self.cursor.execute("INSERT INTO venta (id_cliente, id_usuario, fecha, total) VALUES (%s, %s, %s, %s)", (id_cliente, id_usuario, fecha, total))
            self.conn.commit()

            #obtener el id de la venta
            self.cursor.execute("SELECT MAX(id) FROM venta")
            id_venta = self.cursor.fetchone()[0]
            return id_venta

        except (Exception, psycopg2.DatabaseError) as error:
            raise Exception(f"Error creando venta: {error}")
        

        
    def create_detalle_venta(self, id_venta, id_producto, cantidad):
        try:
            #discount stock
            self.cursor.execute("SELECT stock FROM producto WHERE id = %s", (id_producto,))
            stock = self.cursor.fetchone()[0]
            if stock < cantidad:
                raise Exception("No hay suficiente stock para el producto")
            self.cursor.execute("UPDATE producto SET stock = %s WHERE id = %s", (stock - cantidad, id_producto))
            self.conn.commit()
            #create detalle_venta
            self.cursor.execute("INSERT INTO venta_detalle (id_venta, id_producto, cantidad) VALUES (%s, %s, %s)", (id_venta, id_producto, cantidad))
            self.conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            raise Exception(f"Error creando detalle de venta: {error}")
    
    def __del__(self):
        self.cursor.close()
        self.conn.close()