from tkinter import ttk
import tkinter as tk
from tkinter import messagebox

from Interface.db_repo import DbRepo

class BuscarClienteToplevel(tk.Toplevel):
    def __init__(self, parent, db_repo : DbRepo):
        super().__init__(parent)
        self.parent = parent
        self.db_repo = db_repo
        self.title("Buscar Cliente")
        self.geometry("500x400")
        self.build_ui()

    def build_ui(self):
    # Label y Entry para el nombre del cliente
        ttk.Label(self, text="Nombre del Cliente:").pack(padx=10, pady=5)
        self.nombre_cliente_entry = ttk.Entry(self)
        self.nombre_cliente_entry.pack(padx=10, pady=5)

        # Botón de buscar
        ttk.Button(self, text="Buscar", 
                command=lambda: self.buscar_cliente(self.nombre_cliente_entry.get(), self.tree_resultados)).pack(pady=5)

        # Treeview para mostrar los resultados de la búsqueda
        self.columnas = ("ID", "Nombre", "Dirección", "Email", "Teléfono")
        self.tree_resultados = ttk.Treeview(self, columns=self.columnas, show="headings")
        for col in self.columnas:
            self.tree_resultados.heading(col, text=col)
            self.tree_resultados.column(col, width=100)
        
        self.tree_resultados.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree_resultados.bind("<<TreeviewSelect>>", self.seleccionar_cliente)

    

    def buscar_cliente(self, nombre_cliente, tree):
        # Elimina los elementos anteriores en el Treeview
        tree.delete(*tree.get_children())

        try:
            # Llamada al repositorio para obtener los clientes por nombre
            resultados = self.db_repo.buscar_cliente_por_nombre(nombre_cliente)
            
            # Si hay resultados, los agregamos al Treeview
            if resultados:
                for cliente in resultados:
                    tree.insert("", "end", values=(cliente.id, cliente.nombre, cliente.direccion, cliente.email, cliente.telefono))
            else:
                messagebox.showinfo("Información", "No se encontraron clientes con ese nombre.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar clientes: {e}")

    def seleccionar_cliente(self, event):
        # Obtiene el ID del cliente seleccionado
        item = self.tree_resultados.selection()[0]
        id_cliente = self.tree_resultados.item(item)["values"][0]

        # Llama al método seleccionar_cliente del padre
        self.parent.cliente_seleccionado=self.db_repo.obtener_cliente_por_id(id_cliente)
        self.parent.btn_cliente.config(text="Cliente: " + self.parent.cliente_seleccionado.nombre)
        self.destroy()