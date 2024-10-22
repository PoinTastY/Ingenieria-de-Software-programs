import tkinter as tk
from tkinter import ttk, messagebox

from Interface.db_repo import DbRepo

class ClientesTab(tk.Frame):
    def __init__(self, parent, db_repo: DbRepo):
        super().__init__(parent)
        self.db_repo = db_repo
        self.parent = parent
        self.pack()
        self.build_ui()
        
    def build_ui(self):
        # ID Cliente
        ttk.Label(self, text="ID Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.id_cliente_entry = ttk.Entry(self, state="readonly")
        self.id_cliente_entry.grid(row=0, column=1, padx=5, pady=5)

        # Botón Obtener ID
        ttk.Button(self, text="Obtener ID", command=self.obtener_siguiente_id).grid(row=0, column=2, padx=5, pady=5)

        # Nombre
        ttk.Label(self, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.nombre_cliente_entry = ttk.Entry(self)
        self.nombre_cliente_entry.grid(row=1, column=1, padx=5, pady=5)

        # Apellido
        ttk.Label(self, text="Apellido:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.apellido_cliente_entry = ttk.Entry(self)
        self.apellido_cliente_entry.grid(row=2, column=1, padx=5, pady=5)

        # Dirección
        ttk.Label(self, text="Dirección:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.direccion_cliente_entry = ttk.Entry(self)
        self.direccion_cliente_entry.grid(row=3, column=1, padx=5, pady=5)

        # Email
        ttk.Label(self, text="Email:").grid(row=0, column=3, padx=5, pady=5, sticky="e")
        self.email_cliente_entry = ttk.Entry(self)
        self.email_cliente_entry.grid(row=0, column=4, padx=5, pady=5)

        # Teléfono
        ttk.Label(self, text="Teléfono:").grid(row=1, column=3, padx=5, pady=5, sticky="e")
        self.telefono_cliente_entry = ttk.Entry(self)
        self.telefono_cliente_entry.grid(row=1, column=4, padx=5, pady=5)

        # Botones de Operaciones
        button_frame = ttk.Frame(self)
        button_frame.grid(row=4, column=0, columnspan=5, pady=10)

        ttk.Button(button_frame, text="Registrar", command=self.registrar_cliente).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Buscar", command=self.buscar_cliente).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="Editar", command=self.editar_cliente).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(button_frame, text="Eliminar", command=self.eliminar_cliente).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(button_frame, text="Limpiar", command=self.limpiar_campos_cliente).grid(row=0, column=4, padx=5, pady=5)

        # Tabla de Clientes
        self.tree_clientes = ttk.Treeview(self, columns=("ID", "Nombre", "Dirección", "Email", "Teléfono"), show='headings')
        self.tree_clientes.heading("ID", text="ID")
        self.tree_clientes.heading("Nombre", text="Nombre")
        self.tree_clientes.heading("Dirección", text="Dirección")
        self.tree_clientes.heading("Email", text="Email")
        self.tree_clientes.heading("Teléfono", text="Teléfono")
        
        # Configura las columnas para que se adapten al tamaño de la ventana
        self.tree_clientes.column("ID", width=50)
        self.tree_clientes.column("Nombre", width=150)
        self.tree_clientes.column("Dirección", width=200)
        self.tree_clientes.column("Email", width=150)
        self.tree_clientes.column("Teléfono", width=100)

        # Empaqueta la tabla
        self.tree_clientes.grid(row=5, column=0, columnspan=5, padx=20, pady=10, sticky="nsew")

        # Agrega comportamiento de selección en la tabla
        self.tree_clientes.bind("<<TreeviewSelect>>", self.seleccionar_cliente)


    def obtener_siguiente_id(self):
        id = self.db_repo.obtener_siguiente_id_cliente()
        self.id_cliente_entry.config(state="normal")
        self.id_cliente_entry.delete(0, tk.END)
        self.id_cliente_entry.insert(0, id)
        self.id_cliente_entry.config(state="readonly")

    def registrar_cliente(self):
        try:
            id = self.id_cliente_entry.get()
            nombre = self.nombre_cliente_entry.get()
            apellido = self.apellido_cliente_entry.get()
            direccion = self.direccion_cliente_entry.get()
            email = self.email_cliente_entry.get()
            telefono = self.telefono_cliente_entry.get()
            
            # Cambié self.hotel por self.db_repo para acceder a la base de datos
            if self.db_repo.registrar_cliente(id, nombre, apellido, direccion, email, telefono):
                messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
                self.actualizar_tabla_clientes()
                self.limpiar_campos_cliente()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el cliente: {e}")

    def buscar_cliente(self):
        nombre = self.nombre_cliente_entry.get()
        resultados = self.db_repo.buscar_cliente_por_nombre(nombre)
        self.tree_clientes.delete(*self.tree_clientes.get_children())
        for id_cliente, cliente in resultados:
            self.tree_clientes.insert("", "end", values=(id_cliente, cliente['nombre'], cliente['direccion'], cliente['email'], cliente['telefono']))
        if not resultados:
            messagebox.showinfo("Información", "No se encontraron clientes con ese nombre.")

    def editar_cliente(self):
        selected = self.tree_clientes.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un cliente de la tabla.")
            return
        id_cliente = self.id_cliente_entry.get()
        nombre = self.nombre_cliente_entry.get()
        apellido = self.apellido_cliente_entry.get()
        direccion = self.direccion_cliente_entry.get()
        email = self.email_cliente_entry.get()
        telefono = self.telefono_cliente_entry.get()
        
        if self.db_repo.editar_cliente(id_cliente, nombre, apellido, direccion, email, telefono):
            messagebox.showinfo("Éxito", "Cliente editado correctamente.")
            self.actualizar_tabla_clientes()
            self.limpiar_campos_cliente()
        else:
            messagebox.showerror("Error", "No se pudo editar el cliente.")

    def eliminar_cliente(self):
        try:
            selected = self.tree_clientes.selection()
            if not selected:
                messagebox.showwarning("Advertencia", "Seleccione un cliente de la tabla.")
                return
            id_cliente = self.tree_clientes.item(selected)['values'][0]
            confirm = messagebox.askyesno("Confirmación", "¿Está seguro de eliminar este cliente?")
            if confirm:
                if self.db_repo.eliminar_cliente(id_cliente):
                    messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
                    self.actualizar_tabla_clientes()
                    self.limpiar_campos_cliente()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el cliente.")
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el cliente: {e}")

    def limpiar_campos_cliente(self):
        self.id_cliente_entry.config(state="normal")
        self.id_cliente_entry.delete(0, tk.END)
        self.id_cliente_entry.config(state="readonly")
        self.nombre_cliente_entry.delete(0, tk.END)
        self.apellido_cliente_entry.delete(0, tk.END)
        self.direccion_cliente_entry.delete(0, tk.END)
        self.email_cliente_entry.delete(0, tk.END)
        self.telefono_cliente_entry.delete(0, tk.END)

    def seleccionar_cliente(self, event):
        selected = self.tree_clientes.selection()
        if selected:
            values = self.tree_clientes.item(selected)['values']
            self.id_cliente_entry.config(state="normal")
            self.id_cliente_entry.delete(0, tk.END)
            self.id_cliente_entry.insert(0, values[0])
            self.id_cliente_entry.config(state="readonly")
            self.nombre_cliente_entry.delete(0, tk.END)
            self.nombre_cliente_entry.insert(0, values[1])
            self.apellido_cliente_entry.delete(0, tk.END)
            self.apellido_cliente_entry.insert(0, values[1])
            self.direccion_cliente_entry.delete(0, tk.END)
            self.direccion_cliente_entry.insert(0, values[2])
            self.email_cliente_entry.delete(0, tk.END)
            self.email_cliente_entry.insert(0, values[3])
            self.telefono_cliente_entry.delete(0, tk.END)
            self.telefono_cliente_entry.insert(0, values[4])

    def actualizar_tabla_clientes(self):
        try:
            self.tree_clientes.delete(*self.tree_clientes.get_children())
            # Llamada al repositorio para obtener la lista de clientes (objetos)
            clientes = self.db_repo.obtener_clientes()
            
            # Itera sobre la lista de objetos Cliente y los inserta en el treeview
            for cliente in clientes:
                self.tree_clientes.insert("", "end", values=(cliente.id, cliente.nombre, cliente.direccion, cliente.email, cliente.telefono))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la tabla de clientes: {e}")

