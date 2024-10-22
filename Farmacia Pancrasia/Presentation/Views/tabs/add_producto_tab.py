import tkinter as tk
from tkinter import messagebox

from Interface.db_repo import DbRepo

class AddProductoTab(tk.Frame):
    def __init__(self, parent, db_repo : DbRepo):
        super().__init__(parent)
        self.parent = parent
        self.db_repo = db_repo
        self.pack()
        self.build_ui()
        self.entry_codigo.focus_set()

    def build_ui(self):
         # Etiqueta y entrada para el nombre del producto
        self.label_codigo = tk.Label(self, text="Codigo:")
        self.label_codigo.grid(row=0, column=0, padx=10, pady=10)
        self.entry_codigo = tk.Entry(self)
        self.entry_codigo.grid(row=0, column=1, padx=10, pady=10)

        # Botón para buscar producto
        self.boton_buscar = tk.Button(self, text="Buscar", command= lambda : self.buscar_producto(None))
        self.boton_buscar.grid(row=0, column=2, padx=10, pady=10)
        self.boton_buscar.bind("<Return>", self.buscar_producto)
        
        # Etiqueta y entrada para el precio
        self.label_descripcion = tk.Label(self, text="Descripcion:")
        self.label_descripcion.grid(row=1, column=0, padx=10, pady=10)
        self.entry_descripcion = tk.Entry(self, state="disabled")
        self.entry_descripcion.grid(row=1, column=1, padx=10, pady=10)
        
        # Etiqueta y entrada para la cantidad
        self.label_precio = tk.Label(self, text="Precio:")
        self.label_precio.grid(row=2, column=0, padx=10, pady=10)
        self.entry_precio = tk.Entry(self, state="disabled")
        self.entry_precio.grid(row=2, column=1, padx=10, pady=10)

        # Etiqueta y entrada para el stock
        self.label_stock = tk.Label(self, text="Stock:")
        self.label_stock.grid(row=3, column=0, padx=10, pady=10)
        self.entry_stock = tk.Entry(self, state="disabled")
        self.entry_stock.grid(row=3, column=1, padx=10, pady=10)
        
        # Botón para agregar producto
        self.boton_agregar = tk.Button(self, text="Agregar Producto", state="disabled", command=self.create_product)
        self.boton_agregar.grid(row=4, columnspan=2, padx=10, pady=10)

    def buscar_producto(self, event):
        product = self.entry_codigo.get()

        if not product:
            messagebox.showerror("Error", "Ingrese un código de producto")
            self.clear_inputs()
            self.entry_codigo.focus_set()
            return
        try:
            fetched_product = self.db_repo.read_producto(self.entry_codigo.get())
            if fetched_product:
                self.show_found_product(fetched_product)
            else:
                self.clear_inputs()
                self.entry_descripcion.config(state="normal")
                self.entry_precio.config(state="normal")
                self.entry_stock.config(state="normal")
                self.boton_agregar.config(state="normal", text="Agregar Producto")

        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def show_found_product(self, fetched_product):
        self.clear_inputs()
        self.entry_descripcion.config(state="normal")
        self.entry_precio.config(state="normal")
        self.entry_stock.config(state="normal")
        self.boton_agregar.config(state="normal", text="Guardar Cambios")

        self.entry_descripcion.delete(0, tk.END)
        self.entry_descripcion.insert(0, fetched_product[2])
        self.entry_precio.delete(0, tk.END)
        self.entry_precio.insert(0, fetched_product[3])
        self.entry_stock.delete(0, tk.END)
        self.entry_stock.insert(0, fetched_product[4])

        self.entry_stock.config(state="disabled")
    
    def create_product(self):
        codigo = self.entry_codigo.get()
        descripcion = self.entry_descripcion.get()
        precio = self.entry_precio.get()
        stock = self.entry_stock.get()

        # Validate inputs
        if not codigo or not descripcion or not precio or not stock:
            messagebox.showerror("Error", "Llena todos los campos")
            return

        try:
            self.db_repo.create_producto(codigo, descripcion, precio, stock)
            messagebox.showinfo("Exito", "Producto Guardado")

            self.clear_inputs()
            self.entry_codigo.delete(0, tk.END)
            
            self.entry_codigo.focus_set()

        except Exception as e:
            messagebox.showerror("Error", str(e))
    def clear_inputs(self):
        # Clear inputs
        self.entry_stock.config(state="normal")
        self.entry_descripcion.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)

        self.entry_descripcion.config(state="disabled")
        self.entry_precio.config(state="disabled")
        self.entry_stock.config(state="disabled")
        self.boton_agregar.config(state="disabled", text="Agregar Producto")
