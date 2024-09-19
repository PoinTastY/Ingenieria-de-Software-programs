import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Clases para gestionar los datos
class Cliente:
    def __init__(self, cliente_id, nombre, direccion, email, telefono):
        self.cliente_id = cliente_id
        self.nombre = nombre
        self.direccion = direccion
        self.email = email
        self.telefono = telefono

# Lista vacía de clientes
clientes = []
cliente_en_edicion = None  # Variable para almacenar el cliente que se está editando

# Crear la ventana principal
root = tk.Tk()
root.title("Sistema de Gestión")

# Crear un objeto Notebook (para las pestañas)
notebook = ttk.Notebook(root)

# Crear los frames para cada pestaña
cliente_frame = ttk.Frame(notebook)
habitacion_frame = ttk.Frame(notebook)

# Añadir los frames al notebook
notebook.add(cliente_frame, text="Cliente")
notebook.add(habitacion_frame, text="Habitación")

# Empaquetar el notebook
notebook.pack(expand=1, fill="both")

# ---- Funcionalidades para Clientes ----

def obtener_siguiente_id():
    """Devuelve el siguiente ID disponible basado en los clientes existentes."""
    if clientes:
        return max(cliente.cliente_id for cliente in clientes) + 1
    return 1

def registrar_cliente():
    global cliente_en_edicion
    if cliente_en_edicion is not None:
        messagebox.showerror("Error", "Estás en modo edición, guarda los cambios primero")
        return
    
    id_cliente = obtener_siguiente_id()
    nombre = entry_nombre.get()
    direccion = entry_direccion.get()
    email = entry_email.get()
    telefono = entry_telefono.get()
    
    if nombre and direccion and email and telefono:
        nuevo_cliente = Cliente(id_cliente, nombre, direccion, email, telefono)
        clientes.append(nuevo_cliente)
        messagebox.showinfo("Éxito", f"Cliente {nombre} registrado exitosamente")
        limpiar_campos()
        mostrar_clientes()
    else:
        messagebox.showerror("Error", "Todos los campos son obligatorios")

def buscar_cliente():
    global cliente_en_edicion
    id_buscar = entry_id.get()
    if id_buscar.isdigit():
        id_buscar = int(id_buscar)
        for cliente in clientes:
            if cliente.cliente_id == id_buscar:
                entry_nombre.delete(0, tk.END)
                entry_nombre.insert(0, cliente.nombre)
                entry_direccion.delete(0, tk.END)
                entry_direccion.insert(0, cliente.direccion)
                entry_email.delete(0, tk.END)
                entry_email.insert(0, cliente.email)
                entry_telefono.delete(0, tk.END)
                entry_telefono.insert(0, cliente.telefono)
                
                # Al encontrar el cliente, habilitamos el modo de edición
                cliente_en_edicion = cliente
                btn_guardar.config(state="normal")  # Habilitar el botón Guardar
                btn_registrar.config(state="disabled")  # Deshabilitar el botón Registrar
                return
        messagebox.showerror("Error", f"No se encontró al cliente con ID {id_buscar}")
    else:
        messagebox.showerror("Error", "El ID debe ser un número")

def guardar_cambios():
    global cliente_en_edicion
    if cliente_en_edicion is not None:
        cliente_en_edicion.nombre = entry_nombre.get()
        cliente_en_edicion.direccion = entry_direccion.get()
        cliente_en_edicion.email = entry_email.get()
        cliente_en_edicion.telefono = entry_telefono.get()
        
        messagebox.showinfo("Éxito", f"Datos del cliente ID {cliente_en_edicion.cliente_id} actualizados")
        cliente_en_edicion = None
        mostrar_clientes()
        limpiar_campos()
        btn_guardar.config(state="disabled")  # Deshabilitar el botón Guardar
        btn_registrar.config(state="normal")  # Habilitar el botón Registrar
    else:
        messagebox.showerror("Error", "No hay cliente en edición")

def eliminar_cliente():
    id_buscar = entry_id.get()
    if id_buscar.isdigit():
        id_buscar = int(id_buscar)
        for cliente in clientes:
            if cliente.cliente_id == id_buscar:
                clientes.remove(cliente)
                messagebox.showinfo("Éxito", f"Cliente con ID {id_buscar} eliminado")
                limpiar_campos()
                mostrar_clientes()
                return
        messagebox.showerror("Error", f"No se encontró al cliente con ID {id_buscar}")
    else:
        messagebox.showerror("Error", "El ID debe ser un número")

def limpiar_campos():
    global cliente_en_edicion
    entry_id.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_direccion.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    cliente_en_edicion = None

def mostrar_clientes():
    for item in cliente_tree.get_children():
        cliente_tree.delete(item)
    for cliente in clientes:
        cliente_tree.insert('', 'end', values=(cliente.cliente_id, cliente.nombre, cliente.direccion, cliente.email, cliente.telefono))

# ---- Interfaz para Clientes ----
# Etiquetas y entradas
label_id = ttk.Label(cliente_frame, text="ID del Cliente:")
label_id.pack(pady=5)
entry_id = ttk.Entry(cliente_frame)
entry_id.pack(pady=5)

label_nombre = ttk.Label(cliente_frame, text="Nombre:")
label_nombre.pack(pady=5)
entry_nombre = ttk.Entry(cliente_frame)
entry_nombre.pack(pady=5)

label_direccion = ttk.Label(cliente_frame, text="Dirección:")
label_direccion.pack(pady=5)
entry_direccion = ttk.Entry(cliente_frame)
entry_direccion.pack(pady=5)

label_email = ttk.Label(cliente_frame, text="Email:")
label_email.pack(pady=5)
entry_email = ttk.Entry(cliente_frame)
entry_email.pack(pady=5)

label_telefono = ttk.Label(cliente_frame, text="Teléfono:")
label_telefono.pack(pady=5)
entry_telefono = ttk.Entry(cliente_frame)
entry_telefono.pack(pady=5)

# Botones
btn_registrar = ttk.Button(cliente_frame, text="Registrar Cliente", command=registrar_cliente)
btn_registrar.pack(pady=5)

btn_buscar = ttk.Button(cliente_frame, text="Buscar Cliente", command=buscar_cliente)
btn_buscar.pack(pady=5)

btn_guardar = ttk.Button(cliente_frame, text="Guardar Cambios", command=guardar_cambios, state="disabled")
btn_guardar.pack(pady=5)

btn_eliminar = ttk.Button(cliente_frame, text="Eliminar Cliente", command=eliminar_cliente)
btn_eliminar.pack(pady=5)

# Tabla para mostrar clientes
cliente_tree = ttk.Treeview(cliente_frame, columns=('ID', 'Nombre', 'Dirección', 'Email', 'Teléfono'), show='headings')
cliente_tree.heading('ID', text='ID')
cliente_tree.heading('Nombre', text='Nombre')
cliente_tree.heading('Dirección', text='Dirección')
cliente_tree.heading('Email', text='Email')
cliente_tree.heading('Teléfono', text='Teléfono')
cliente_tree.pack(expand=1, fill='both', padx=10, pady=10)

#desarrolo de habitaciones :)
label_numero_habitacion = ttk.Label(habitacion_frame, text="Ingrese número de habitación:")
label_numero_habitacion.grid(row=1, column=0, padx=20, pady=20)
# Campo de entrada para el número de habitación
entry_numero_habitacion = ttk.Entry(habitacion_frame)
entry_numero_habitacion.grid(row=1, column=1, padx=10, pady=10)

# Texto para "Número"
label_numero = ttk.Label(habitacion_frame, text="Numero:")
label_numero.grid(row=3, column=0, padx=(10, 2), pady=10, sticky='e')

# Cuadro de entrada para el número (editable y más pequeño)
entry_numero = ttk.Entry(habitacion_frame, width=10)  # Ajusta el tamaño del cuadro de entrada
entry_numero.grid(row=3, column=1, padx=(2, 10), pady=10, sticky='w')

btn_buscar_habitacion = ttk.Button(habitacion_frame, text="Buscar")
btn_buscar_habitacion.grid(row=1, column=2, padx=30, pady=30)


# Cuadro de texto para mostrar el ID de la habitación (no editable)
# Texto para "Habitación ID"
label_habitacion_id = ttk.Label(habitacion_frame, text="Habitación ID:")
label_habitacion_id.grid(row=2, column=0, padx=(10, 2), pady=10, sticky='e')  # `sticky='e'` alinea el texto a la derecha

# Cuadro de texto para mostrar el ID de la habitación (no editable y más pequeño)
entry_habitacion_id = ttk.Entry(habitacion_frame, state='readonly', width=10)  # Ajusta el tamaño del cuadro de entrada
entry_habitacion_id.grid(row=2, column=1, padx=(2, 10), pady=10, sticky='w')  # `sticky='w'` alinea el cuadro a la izquier

# para el selector ocupado libre 
# Texto para "Estado"
# label_estado_habitacion = ttk.Label(habitacion_frame, text="Estado:")
# label_estado_habitacion.grid(row=2, column=1, padx=(10, 2), pady=10, sticky='e')

# Cuadro selector para "Disponible" y "Ocupado"
# estado_var = tk.StringVar()  # Variable para almacenar la selección
# combobox_estado = ttk.Combobox(habitacion_frame, textvariable=estado_var, state="readonly", width=10)
# combobox_estado['values'] = ("Disponible", "Ocupado")  # Opciones del combobox
# combobox_estado.set("Disponible")  # Establece "Disponible" como la opción predeterminada
# combobox_estado.grid(row=2, column=2, padx=(2, 10), pady=10, sticky='w')

# Botón para las habita ciones
btn_nueva_habitacion = tk.Button(habitacion_frame, text="Nueva Habitación", width=15, height=2, bg="light grey")
btn_nueva_habitacion.grid(row=4, column=1, padx=10, pady=10, sticky='e')

# # Botón para editar habitaciones
# btn_editar_habitacion = tk.Button(habitacion_frame, text="Editar", width=15, height=2, bg="light grey")
# btn_editar_habitacion.grid(row=4, column=2, padx=10, pady=10, sticky='w')

class habitacion:
    def __init__(self, id : int, nombre : str):
        self.habitacion_id = id
        self.nombre = nombre
        self.disponible = "Disponible"

id_habitaciones = 1
lista_habitaciones = []

def nueva_habitacion():
    global id_habitaciones
    nombre_habitacion = entry_numero.get()
    if not nombre_habitacion:
        messagebox.showerror("Error", "El número de la habitación es obligatorio")
        return
    for room in lista_habitaciones:
        if room.nombre == nombre_habitacion:
            messagebox.showerror("Error", "El número de la habitación ya existe")
            return
    
    nueva_hab = habitacion(id_habitaciones, nombre_habitacion)  # Crea una nueva habitación con ID incremental
    lista_habitaciones.append(nueva_hab)
    limpiar_campos_habitacion()

    messagebox.showinfo("Nueva Habitación", f"Se ha creado una nueva habitación con ID: {nueva_hab.habitacion_id}")
    id_habitaciones += 1
    mostrar_habitacion_id(id_habitaciones)

# Función para limpiar los campos
def limpiar_campos_habitacion():
    entry_numero.delete(0, tk.END)

# Mostrar ID en el campo "Habitación ID"
def mostrar_habitacion_id(id_habitacion):
    entry_habitacion_id.config(state='normal')
    entry_habitacion_id.delete(0, tk.END)
    entry_habitacion_id.insert(0, id_habitacion)
    entry_habitacion_id.config(state='readonly')

mostrar_habitacion_id(id_habitaciones)

# Función para actualizar la habitación con los datos ingresados por el usuario
def actualizar_habitacion():
    id_habitacion = int(entry_habitacion_id.get())
    for hab in lista_habitaciones:
        if hab.habitacion_id == id_habitacion:
            hab.numero = entry_numero.get()
            messagebox.showinfo("Habitación Actualizada", f"Habitación ID {hab.habitacion_id} actualizada con éxito")
            break

# Asignar el comando al botón "Nueva Habitación"
btn_nueva_habitacion.config(command=nueva_habitacion)

# Asignar el comando al botón "Editar Habitación"
# btn_editar_habitacion.config(command=actualizar_habitacion)
# Botón de "Buscar"


# Función para buscar la habitación
def buscar_habitacion():
    id_buscar = entry_numero_habitacion.get()  # Usar el campo de número para buscar
    print(f"Buscando habitación con ID: {id_buscar}")  # Depuración

    if id_buscar.isdigit():
        id_buscar = int(id_buscar)
        for hab in lista_habitaciones:
            if hab.habitacion_id == id_buscar:
                print(f"Encontrada habitación: ID {hab.habitacion_id}, Numero {hab.numero}, Estado {'Disponible' if hab.disponible else 'Ocupado'}")  # Depuración
                
                # Mostrar los datos de la habitación en los campos correspondientes
                mostrar_habitacion_id(hab.habitacion_id)  # Actualizar el campo de ID
                entry_numero.delete(0, tk.END)
                entry_numero.insert(0, hab.numero)  # Actualizar el campo de número
                
                # Actualizar el estado en el combobox según la disponibilidad
                if hab.disponible:
                    combobox_estado.set("Disponible")  # Asegúrate de que el valor esté en la lista de opciones
                else:
                    combobox_estado.set("Ocupado")  # Asegúrate de que el valor esté en la lista de opciones
                
                return
        messagebox.showerror("Error", f"No se encontró la habitación con ID {id_buscar}")
    else:
        messagebox.showerror("Error", "El ID debe ser un número válido")



btn_buscar_habitacion.config(command=buscar_habitacion)

# ---- definicion reservaciones ----
lista_reservaciones = []
id_reservaciones = 1

class reservacion:
    def __init__(self, id : int, id_cliente : int, id_habitacion : int, fecha_salida : datetime, costo : float) -> None:
        self.id = id
        self.id_cliente = id_cliente
        self.id_habitacion = id_habitacion
        self.fecha_reservacion = datetime.datetime.now().date().strftime("%Y-%m-%d")
        self.hora_reservacion = datetime.datetime.now().time().strftime("%H:%M:%S")
        self.fecha_salida = fecha_salida.date().strftime("%Y-%m-%d")
        self.costo = costo
        

class ReservacionesTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Labels y Entradas para buscar y detalles de la reservación
        ttk.Label(self, text="Ingrese Reservación:").grid(row=0, column=0, padx=5, pady=5)
        self.reservacion_busqueda = ttk.Entry(self)
        self.reservacion_busqueda.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self, text="Buscar Reservacion", command=self.buscar_reservacion).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(self, text="Reservacion ID:").grid(row=1, column=0, padx=5, pady=5)
        self.reservacion_id_entry = ttk.Entry(self, state = tk.DISABLED)
        self.reservacion_id_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="Cliente ID:").grid(row=2, column=0, padx=5, pady=5)
        self.cliente_id_entry = ttk.Combobox(self, values=list(map(lambda cliente: cliente.cliente_id, clientes)),  state=tk.DISABLED)
        self.cliente_id_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text="Habitacion ID:").grid(row=3, column=0, padx=5, pady=5)
        self.habitacion_id_entry = ttk.Combobox(self, values=list(map(lambda habitacion: habitacion.habitacion_id, lista_habitaciones)), state=tk.DISABLED)
        self.habitacion_id_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self, text="Fecha Reservacion (YYYY-mm-dd):").grid(row=4, column=0, padx=5, pady=5)
        self.fecha_reservacion_entry = ttk.Entry(self, state=tk.DISABLED)
        self.fecha_reservacion_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self, text="Fecha Salida (YYYY-mm-dd):").grid(row=5, column=0, padx=5, pady=5)
        self.fecha_salida_entry = ttk.Entry(self, state=tk.DISABLED)
        self.fecha_salida_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(self, text="Hora Reservacion (H:M:S):").grid(row=6, column=0, padx=5, pady=5)
        self.hora_reservacion_entry = ttk.Entry(self, state=tk.DISABLED)
        self.hora_reservacion_entry.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(self, text="Costo:").grid(row=7, column=0, padx=5, pady=5)
        self.costo_entry = ttk.Entry(self, state=tk.DISABLED)
        self.costo_entry.grid(row=7, column=1, padx=5, pady=5)

        # Botones de control
        self.botones_frame = ttk.Frame(self)
        self.botones_frame.grid(row=8, column=0, columnspan=3, pady=10)

        self.btn_new_reservacion = tk.Button(self, text="Nueva Reservacion", command=self.nueva_reservacion)
        self.btn_new_reservacion.grid(row=8, column=0, padx=5)
        self.btn_save_reservacion = tk.Button(self, text="Reservar", state= tk.DISABLED, command=self.guardar_reservacion)
        self.btn_save_reservacion.grid(row=8, column=1, padx=5)
        self.btn_cancel_reservacion = tk.Button(self, text="Cancelar Reservacion", state= tk.DISABLED, command=self.cancelar_reservacion)
        self.btn_cancel_reservacion.grid(row=8, column=2, padx=5)
        self.btn_edit_reservacion = tk.Button(self, text="Editar", state= tk.DISABLED, command=self.editar_reservacion)
        self.btn_edit_reservacion.grid(row=8, column=3, padx=5)

        #listar reservaciones
        self.reservaciones_tree = ttk.Treeview(self, columns=('ID', 'Cliente ID', 'Habitacion ID', 'Fecha Reservacion', 'Fecha Salida', 'Hora Reservacion', 'Costo'), show='headings')
        self.reservaciones_tree.heading('ID', text='ID')
        self.reservaciones_tree.heading('Cliente ID', text='Cliente ID')
        self.reservaciones_tree.heading('Habitacion ID', text='Habitacion ID')
        self.reservaciones_tree.heading('Fecha Reservacion', text='Fecha Reservacion')
        self.reservaciones_tree.heading('Fecha Salida', text='Fecha Salida')
        self.reservaciones_tree.heading('Hora Reservacion', text='Hora Reservacion')
        self.reservaciones_tree.heading('Costo', text='Costo')
        self.reservaciones_tree.grid(row=9, column=0, columnspan=3, padx=10, pady=10)
        #link lista_reservaciones to the treeview
        for reservacion in lista_reservaciones:
            self.reservaciones_tree.insert('', 'end', values=(reservacion.id, reservacion.id_cliente, reservacion.id_habitacion, reservacion.fecha_reservacion, reservacion.fecha_salida, reservacion.hora_reservacion, reservacion.costo))

    def update_reservaciones_tree(self):
        for item in self.reservaciones_tree.get_children():
            self.reservaciones_tree.delete(item)
        for reservacion in lista_reservaciones:
            self.reservaciones_tree.insert('', 'end', values=(reservacion.id, reservacion.id_cliente, reservacion.id_habitacion, reservacion.fecha_reservacion, reservacion.fecha_salida, reservacion.hora_reservacion, reservacion.costo))

    #on appearing method to update the comboboxes
    def on_appearing(self):
        self.cliente_id_entry['values'] = list(map(lambda cliente: cliente.cliente_id, clientes))
        self.habitacion_id_entry['values'] = list(map(lambda habitacion: habitacion.habitacion_id, lista_habitaciones))



    def editar_reservacion(self):
        #enable all entries for editing
        self.reservacion_id_entry.config(state=tk.NORMAL)
        self.cliente_id_entry.config(state=tk.NORMAL)
        self.habitacion_id_entry.config(state=tk.NORMAL)
        self.fecha_reservacion_entry.config(state=tk.NORMAL)
        self.fecha_salida_entry.config(state=tk.NORMAL)
        self.hora_reservacion_entry.config(state=tk.NORMAL)
        self.costo_entry.config(state=tk.NORMAL)
        #and the buttons
        self.btn_save_reservacion.config(state=tk.NORMAL)
        self.btn_cancel_reservacion.config(state=tk.NORMAL)
        self.btn_edit_reservacion.config(state=tk.DISABLED)

    def cancelar_reservacion(self):
        #if all entries have content, then change current reservacion status to "cancelled"
        #first, check if the reservacion exists
        id_reservacion = self.reservacion_id_entry.get()
        if id_reservacion.isdigit():
            id_reservacion = int(id_reservacion)
            for res in lista_reservaciones:
                if res.id == id_reservacion:
                    res.estado = "cancelled"
                    messagebox.showinfo("Reservación", f"Reservación con ID {id_reservacion} cancelada exitosamente")
                    self.update_reservaciones_tree()
                    return
            messagebox.showerror("Error", f"No se encontró la reservación con ID {id_reservacion}")


    def guardar_reservacion(self):
        global id_reservaciones
        self.btn_new_reservacion.config(state=tk.NORMAL)
        id_reservacion = self.reservacion_id_entry.get()
        id_cliente = self.cliente_id_entry.get()
        id_habitacion = self.habitacion_id_entry.get()
        fecha_reservacion = self.fecha_reservacion_entry.get()
        fecha_salida = self.fecha_salida_entry.get()
        hora_reservacion = self.hora_reservacion_entry.get()
        costo = self.costo_entry.get()

       


        try:
            fecha_reservacion = datetime.datetime.strptime(fecha_reservacion, "%Y-%m-%d")
            fecha_salida = datetime.datetime.strptime(fecha_salida, "%Y-%m-%d")
        except ValueError as e:
            messagebox.showerror("Error", f"Error en parsear las fechas de entrada y salida: {e}")
            return
        
        if(not(fecha_reservacion < fecha_salida)):
            messagebox.showerror("Error", "La fecha de reservacion debe ser menor a la fecha de salida")
            return
        


        fecha_reservacion = self.fecha_reservacion_entry.get()
        fecha_salida = self.fecha_salida_entry.get()

        if id_reservacion and id_cliente and id_habitacion and fecha_reservacion and fecha_salida and hora_reservacion and costo:
            if id_reservacion.isdigit() and id_cliente.isdigit() and id_habitacion.isdigit():
                id_reservacion = int(id_reservacion)
                id_cliente = int(id_cliente)
                id_habitacion = int(id_habitacion)
                costo = float(costo)
                for res in lista_reservaciones:
                    if res.id == id_reservacion:
                        messagebox.showerror("Error", f"Ya existe una reservación con ID {id_reservacion}")
                        return
                     #validar el estado de la habitacion
                index = 0
                for habitacion in lista_habitaciones:
                    if(habitacion.habitacion_id == int(id_habitacion)):
                        if(habitacion.disponible == "Ocupado"):
                            messagebox.showerror("ERROR", "La habitacion esta ocupada, seleccione otra")
                            return
                        else:
                            lista_habitaciones[index].disponible = "Ocupado"
                        index += 1
                nueva_reservacion = reservacion(id_reservacion, id_cliente, id_habitacion, datetime.datetime.strptime(fecha_salida, "%Y-%m-%d"), costo)
                lista_reservaciones.append(nueva_reservacion)
                messagebox.showinfo("Reservación", f"Reservación con ID {id_reservacion} creada exitosamente")
                id_reservaciones += 1
                self.nueva_reservacion()
                self.update_reservaciones_tree()
            else:
                messagebox.showerror("Error", "ID de la reservación, cliente y habitación deben ser números")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

        print(lista_habitaciones)
        self.btn_save_reservacion.config(state=tk.DISABLED)
        self.btn_cancel_reservacion.config(state=tk.DISABLED)
        self.btn_edit_reservacion.config(state=tk.DISABLED)
        self.btn_new_reservacion.config(state=tk.NORMAL)
        

    def nueva_reservacion(self):
        global id_reservaciones
        self.reservacion_id_entry.config(state=tk.NORMAL)
        self.reservacion_id_entry.delete(0, tk.END)
        self.reservacion_id_entry.insert(0, id_reservaciones)
        self.reservacion_id_entry.config(state=tk.DISABLED)

        self.btn_new_reservacion.config(state=tk.DISABLED)

        self.cliente_id_entry.config(state=tk.NORMAL)
        self.cliente_id_entry.delete(0, tk.END)
        self.cliente_id_entry.insert(0, "")

        self.habitacion_id_entry.config(state=tk.NORMAL)
        self.habitacion_id_entry.delete(0, tk.END)
        self.habitacion_id_entry.insert(0, "")

        self.fecha_reservacion_entry.config(state=tk.NORMAL)
        self.fecha_reservacion_entry.delete(0, tk.END)
        self.fecha_reservacion_entry.insert(0, "")

        self.fecha_salida_entry.config(state=tk.NORMAL)
        self.fecha_salida_entry.delete(0, tk.END)
        self.fecha_salida_entry.insert(0, "")

        self.hora_reservacion_entry.config(state=tk.NORMAL)
        self.hora_reservacion_entry.delete(0, tk.END)
        self.hora_reservacion_entry.insert(0, "")

        self.costo_entry.config(state=tk.NORMAL)
        self.costo_entry.delete(0, tk.END)
        self.costo_entry.insert(0, "")

        self.btn_save_reservacion.config(state=tk.NORMAL)
        self.btn_cancel_reservacion.config(state=tk.NORMAL)
        self.btn_edit_reservacion.config(state=tk.NORMAL)

    def buscar_reservacion(self):
        id_reservacion = self.reservacion_busqueda.get()
        if id_reservacion.isdigit():
            id_reservacion = int(id_reservacion)
            for res in lista_reservaciones:
                if res.id == id_reservacion:
                    self.btn_new_reservacion.config(state=tk.DISABLED)
                    self.reservacion_id_entry.config(state=tk.NORMAL)
                    self.reservacion_id_entry.delete(0, tk.END)
                    self.reservacion_id_entry.insert(0, res.id)
                    self.reservacion_id_entry.config(state=tk.DISABLED)

                    self.cliente_id_entry.config(state=tk.NORMAL)
                    self.cliente_id_entry.delete(0, tk.END)
                    self.cliente_id_entry.insert(0, res.id_cliente)
                    self.cliente_id_entry.config(state=tk.DISABLED)

                    self.habitacion_id_entry.config(state=tk.NORMAL)
                    self.habitacion_id_entry.delete(0, tk.END)
                    self.habitacion_id_entry.insert(0, res.id_habitacion)
                    self.habitacion_id_entry.config(state=tk.DISABLED)

                    self.fecha_reservacion_entry.config(state=tk.NORMAL)
                    self.fecha_reservacion_entry.delete(0, tk.END)
                    self.fecha_reservacion_entry.insert(0, res.fecha_reservacion)
                    self.fecha_reservacion_entry.config(state=tk.DISABLED)

                    self.fecha_salida_entry.config(state=tk.NORMAL)
                    self.fecha_salida_entry.delete(0, tk.END)
                    self.fecha_salida_entry.insert(0, res.fecha_salida)
                    self.fecha_salida_entry.config(state=tk.DISABLED)

                    self.hora_reservacion_entry.config(state=tk.NORMAL)
                    self.hora_reservacion_entry.delete(0, tk.END)
                    self.hora_reservacion_entry.insert(0, res.hora_reservacion)
                    self.hora_reservacion_entry.config(state=tk.DISABLED)

                    self.costo_entry.config(state=tk.NORMAL)
                    self.costo_entry.delete(0, tk.END)
                    self.costo_entry.insert(0, res.costo)
                    self.costo_entry.config(state=tk.DISABLED)

                    self.btn_save_reservacion.config(state= tk.NORMAL)
                    self.btn_cancel_reservacion.config(state=tk.NORMAL)
                    self.btn_edit_reservacion.config(state=tk.NORMAL)
                    return
            messagebox.showerror("Error", f"No se encontró la reservación con ID {id_reservacion}")
        else:
            messagebox.showerror("Error", "El ID de la reservación debe ser un número")

reservacion_frame = ReservacionesTab(notebook)
#trigger the on appearing method when the tab is selected
notebook.bind("<<NotebookTabChanged>>", lambda event: reservacion_frame.on_appearing())
notebook.add(reservacion_frame, text="Reservación")
   
# Ejecutar la aplicación
root.mainloop()

