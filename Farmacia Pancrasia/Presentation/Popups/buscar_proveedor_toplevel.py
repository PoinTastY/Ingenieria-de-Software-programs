from tkinter import ttk
import tkinter as tk
from tkinter import messagebox

from Interface.db_repo import DbRepo

class BuscarProveedorTopLevel(tk.Toplevel):
    def __init__(self, parent, db_repo : DbRepo):
        super().__init__(parent)
        self.parent = parent
        self.db_repo = db_repo
        self.title("Buscar Proveedor")
        self.geometry("500x400")
        self.build_ui()
        self.nombre_proveedor_entry.focus_set()

    def build_ui(self):
    # Label y Entry para el nombre del cliente
        ttk.Label(self, text="Nombre del Proveedor:").pack(padx=10, pady=5)
        self.nombre_proveedor_entry = ttk.Entry(self)
        self.nombre_proveedor_entry.pack(padx=10, pady=5)

        # Botón de buscar
        self.btnBuscar =tk.Button(self, text="Buscar", 
                command=lambda: self.buscar_proveedor(self.nombre_proveedor_entry.get(), self.tree_resultados))
        self.btnBuscar.pack(pady=5)

        # Treeview para mostrar los resultados de la búsqueda
        self.columnas = ("ID", "Nombre", "Telefono")
        self.tree_resultados = ttk.Treeview(self, columns=self.columnas, show="headings")
        for col in self.columnas:
            self.tree_resultados.heading(col, text=col)
            self.tree_resultados.column(col, width=100)
        
        self.tree_resultados.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree_resultados.bind("<<TreeviewSelect>>", self.seleccionar_proveedor)

    def buscar_proveedor(self, nombre_proveedor, tree):
        # Elimina los elementos anteriores en el Treeview
        tree.delete(*tree.get_children())

        try:
            # Llamada al repositorio para obtener los clientes por nombre
            resultados = self.db_repo.buscar_proveedor_por_nombre(nombre_proveedor)
            
            # Si hay resultados, los agregamos al Treeview
            if resultados:
                for proveedor in resultados:
                    tree.insert("", "end", values=(proveedor.id, proveedor.nombre, proveedor.telefono))
            else:
                messagebox.showinfo("Información", "No se encontraron clientes con ese nombre.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar clientes: {e}")

    def seleccionar_proveedor(self, event):
        # Obtiene el ID del cliente seleccionado
        item = self.tree_resultados.selection()[0]
        id_proveedor = self.tree_resultados.item(item)["values"][0]

        proveedor = self.db_repo.obtener_proveedor_por_id(id_proveedor)

        self.parent.proveedor_seleccionado = proveedor
        self.parent.btn_proveedor.config(text="Proveedor: " + proveedor.nombre)
        self.destroy()
