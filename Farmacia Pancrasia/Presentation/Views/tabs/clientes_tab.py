import tkinter as tk
from tkinter import ttk, messagebox

from Interface.db_repo import DbRepo

class ClientesTab(tk.Frame):
    def __init__(self, parent, db_repo: DbRepo, notebook: ttk.Notebook):
        super().__init__(parent)
        self.db_repo = db_repo
        self.notebook = notebook  # Pasamos el notebook aquí
        self.parent = parent
        self.pack()
        self.build_ui()
        self.entry_codigo.focus_set()
        
    def build_ui(self):
        self.clientes_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.clientes_frame, text="Clientes")
        
        # Frame de Formulario
        form_frame = ttk.LabelFrame(self.clientes_frame, text="Información del Cliente")
        form_frame.pack(fill="x", padx=20, pady=10)
        
        # ID Cliente
        ttk.Label(form_frame, text="ID Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.id_cliente_entry = ttk.Entry(form_frame)
        self.id_cliente_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Nombre
        ttk.Label(form_frame, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.nombre_cliente_entry = ttk.Entry(form_frame)
        self.nombre_cliente_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Dirección
        ttk.Label(form_frame, text="Dirección:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.direccion_cliente_entry = ttk.Entry(form_frame)
        self.direccion_cliente_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Email
        ttk.Label(form_frame, text="Email:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.email_cliente_entry = ttk.Entry(form_frame)
        self.email_cliente_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Teléfono
        ttk.Label(form_frame, text="Teléfono:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.telefono_cliente_entry = ttk.Entry(form_frame)
        self.telefono_cliente_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Botones de Operaciones
        button_frame = ttk.Frame(self.clientes_frame)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Button(button_frame, text="Registrar", command=self.registrar_cliente).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Buscar", command=self.buscar_cliente).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="Editar", command=self.editar_cliente).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(button_frame, text="Eliminar", command=self.eliminar_cliente).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(button_frame, text="Limpiar", command=self.limpiar_campos_cliente).grid(row=0, column=4, padx=5, pady=5)
        
        # Tabla de Clientes
        self.tree_clientes = ttk.Treeview(self.clientes_frame, columns=("ID", "Nombre", "Dirección", "Email", "Teléfono"), show='headings')
        self.tree_clientes.heading("ID", text="ID")
        self.tree_clientes.heading("Nombre", text="Nombre")
        self.tree_clientes.heading("Dirección", text="Dirección")
        self.tree_clientes.heading("Email", text="Email")
        self.tree_clientes.heading("Teléfono", text="Teléfono")
        self.tree_clientes.pack(fill="both", padx=20, pady=10, expand=True)
        self.tree_clientes.bind("<<TreeviewSelect>>", self.seleccionar_cliente)

    def registrar_cliente(self):
        id_cliente = self.id_cliente_entry.get()
        nombre = self.nombre_cliente_entry.get()
        direccion = self.direccion_cliente_entry.get()
        email = self.email_cliente_entry.get()
        telefono = self.telefono_cliente_entry.get()
        
        if not id_cliente.isdigit():
            messagebox.showerror("Error", "El ID del cliente debe ser numérico.")
            return
        
        # Cambié self.hotel por self.db_repo para acceder a la base de datos
        if self.db_repo.registrar_cliente(id_cliente, nombre, direccion, email, telefono):
            messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
            self.actualizar_tabla_clientes()
            self.limpiar_campos_cliente()
        else:
            messagebox.showwarning("Advertencia", "El ID del cliente ya existe.")

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
        direccion = self.direccion_cliente_entry.get()
        email = self.email_cliente_entry.get()
        telefono = self.telefono_cliente_entry.get()
        
        if self.db_repo.editar_cliente(id_cliente, nombre, direccion, email, telefono):
            messagebox.showinfo("Éxito", "Cliente editado correctamente.")
            self.actualizar_tabla_clientes()
            self.limpiar_campos_cliente()
        else:
            messagebox.showerror("Error", "No se pudo editar el cliente.")

    def eliminar_cliente(self):
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

    def limpiar_campos_cliente(self):
        self.id_cliente_entry.delete(0, tk.END)
        self.nombre_cliente_entry.delete(0, tk.END)
        self.direccion_cliente_entry.delete(0, tk.END)
        self.email_cliente_entry.delete(0, tk.END)
        self.telefono_cliente_entry.delete(0, tk.END)

    def seleccionar_cliente(self, event):
        selected = self.tree_clientes.selection()
        if selected:
            values = self.tree_clientes.item(selected)['values']
            self.id_cliente_entry.delete(0, tk.END)
            self.id_cliente_entry.insert(0, values[0])
            self.nombre_cliente_entry.delete(0, tk.END)
            self.nombre_cliente_entry.insert(0, values[1])
            self.direccion_cliente_entry.delete(0, tk.END)
            self.direccion_cliente_entry.insert(0, values[2])
            self.email_cliente_entry.delete(0, tk.END)
            self.email_cliente_entry.insert(0, values[3])
            self.telefono_cliente_entry.delete(0, tk.END)
            self.telefono_cliente_entry.insert(0, values[4])

    def actualizar_tabla_clientes(self):
        self.tree_clientes.delete(*self.tree_clientes.get_children())
        for id_cliente, cliente in self.db_repo.obtener_clientes().items():
            self.tree_clientes.insert("", "end", values=(id_cliente, cliente['nombre'], cliente['direccion'], cliente['email'], cliente['telefono']))
