import tkinter as tk
from tkinter import ttk, messagebox

from Interface.db_repo import DbRepo

class ProveedoresTab(tk.Frame):
    def __init__(self, parent, db_repo: DbRepo):
        super().__init__(parent)
        self.db_repo = db_repo
        self.parent = parent
        self.pack()
        self.build_ui()
        
    def build_ui(self):
        # ID Cliente
        ttk.Label(self, text="ID Proveedor:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.id_proveedor_entry = ttk.Entry(self, state="readonly")
        self.id_proveedor_entry.grid(row=0, column=1, padx=5, pady=5)

        # Botón Obtener ID
        ttk.Button(self, text="Obtener ID", command=self.obtener_siguiente_id).grid(row=0, column=2, padx=5, pady=5)

        # Nombre
        ttk.Label(self, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.nombre_proveedor_entry = ttk.Entry(self)
        self.nombre_proveedor_entry.grid(row=1, column=1, padx=5, pady=5)

        # Dirección
        ttk.Label(self, text="Dirección:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.direccion_proveedor_entry = ttk.Entry(self)
        self.direccion_proveedor_entry.grid(row=3, column=1, padx=5, pady=5)

        # Teléfono
        ttk.Label(self, text="Teléfono:").grid(row=1, column=3, padx=5, pady=5, sticky="e")
        self.telefono_proveedor_entry = ttk.Entry(self)
        self.telefono_proveedor_entry.grid(row=1, column=4, padx=5, pady=5)

        # Botones de Operaciones
        button_frame = ttk.Frame(self)
        button_frame.grid(row=4, column=0, columnspan=5, pady=10)

        ttk.Button(button_frame, text="Registrar", command=self.registrar_proveedor).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Editar", command=self.editar_proveedor).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(button_frame, text="Eliminar", command=self.eliminar_proveedor).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(button_frame, text="Limpiar", command=self.limpiar_campos_proveedor).grid(row=0, column=4, padx=5, pady=5)

        # Tabla de Proveedores
        self.tree_proveedores = ttk.Treeview(self, columns=("ID", "Nombre", "Teléfono"), show='headings')
        self.tree_proveedores.heading("ID", text="ID")
        self.tree_proveedores.heading("Nombre", text="Nombre")
        self.tree_proveedores.heading("Teléfono", text="Teléfono")
        
        # Configura las columnas para que se adapten al tamaño de la ventana
        self.tree_proveedores.column("ID", width=50)
        self.tree_proveedores.column("Nombre", width=150)
        self.tree_proveedores.column("Teléfono", width=100)

        # Empaqueta la tabla
        self.tree_proveedores.grid(row=5, column=0, columnspan=5, padx=20, pady=10, sticky="nsew")

        # Agrega comportamiento de selección en la tabla
        self.tree_proveedores.bind("<<TreeviewSelect>>", self.seleccionar_proveedor)


    def obtener_siguiente_id(self):
        id = self.db_repo.obtener_siguiente_id_proveedor()
        self.id_proveedor_entry.config(state="normal")
        self.id_proveedor_entry.delete(0, tk.END)
        self.id_proveedor_entry.insert(0, id)
        self.id_proveedor_entry.config(state="readonly")

    def registrar_proveedor(self):
        try:
            id = self.id_proveedor_entry.get()
            nombre = self.nombre_proveedor_entry.get()
            direccion = self.direccion_proveedor_entry.get()
            telefono = self.telefono_proveedor_entry.get()
            #take 10 characters of the phone number
            telefono = telefono[:10]

            # Cambié self.hotel por self.db_repo para acceder a la base de datos
            if self.db_repo.registrar_proveedor(id, nombre, direccion, telefono):
                messagebox.showinfo("Éxito", "Proveedor registrado correctamente.")
                self.actualizar_tabla_proveedores()
                self.limpiar_campos_proveedor()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el proveedor: {e}")

    def editar_proveedor(self):
        selected = self.tree_proveedores.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un proveedor de la tabla.")
            return
        id_proveedor = self.id_proveedor_entry.get()
        nombre = self.nombre_proveedor_entry.get()
        direccion = self.direccion_proveedor_entry.get()
        telefono = self.telefono_proveedor_entry.get()
        telefono = telefono[:10]
        
        if self.db_repo.editar_proveedor(id_proveedor, nombre, direccion, telefono):
            messagebox.showinfo("Éxito", "Proveedor editado correctamente.")
            self.actualizar_tabla_proveedores()
            self.limpiar_campos_proveedor()
        else:
            messagebox.showerror("Error", "No se pudo editar el Proveedor.")

    def eliminar_proveedor(self):
        try:
            selected = self.tree_proveedores.selection()
            if not selected:
                messagebox.showwarning("Advertencia", "Seleccione un proveedor de la tabla.")
                return
            id_proveedor = self.tree_proveedores.item(selected)['values'][0]
            confirm = messagebox.askyesno("Confirmación", "¿Está seguro de eliminar este proveedor?")
            if confirm:
                if self.db_repo.eliminar_proveedor(id_proveedor):
                    messagebox.showinfo("Éxito", "Proveedor eliminado correctamente.")
                    self.actualizar_tabla_proveedores()
                    self.limpiar_campos_proveedor()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el proveedor.")
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el proveedor: {e}")

    def limpiar_campos_proveedor(self):
        self.id_proveedor_entry.config(state="normal")
        self.id_proveedor_entry.delete(0, tk.END)
        self.id_proveedor_entry.config(state="readonly")
        self.nombre_proveedor_entry.delete(0, tk.END)
        self.direccion_proveedor_entry.delete(0, tk.END)
        self.telefono_proveedor_entry.delete(0, tk.END)

    def seleccionar_proveedor(self, event):
        selected = self.tree_proveedores.selection()
        if selected:
            values = self.tree_proveedores.item(selected)['values']
            self.id_proveedor_entry.config(state="normal")
            self.id_proveedor_entry.delete(0, tk.END)
            self.id_proveedor_entry.insert(0, values[0])
            self.id_proveedor_entry.config(state="readonly")
            self.nombre_proveedor_entry.delete(0, tk.END)
            self.nombre_proveedor_entry.insert(0, values[1])
            self.telefono_proveedor_entry.delete(0, tk.END)
            self.telefono_proveedor_entry.insert(0, values[2])

    def actualizar_tabla_proveedores(self):
        try:
            self.tree_proveedores.delete(*self.tree_proveedores.get_children())
            # Llamada al repositorio para obtener la lista de proveedores (objetos)
            proveedores = self.db_repo.obtener_proveedores()
            
            # Itera sobre la lista de objetos Proveedor y los inserta en el treeview
            for proveedor in proveedores:
                self.tree_proveedores.insert("", "end", values=(proveedor.id, proveedor.nombre, proveedor.telefono))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la tabla de proveedores: {e}")

