import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from Interface.db_repo import DbRepo
from Domain.Entities.cliente import Cliente
from Domain.Entities.usuario import Usuario
from Presentation.Popups.buscar_cliente_toplevel import BuscarClienteToplevel
from Presentation.Popups.buscar_producto_toplevel import BuscarProductoTopLevel

from decimal import Decimal

class VentaTab(tk.Frame):
    def __init__(self, parent, db_repo : DbRepo, usuario : Usuario):
        super().__init__(parent)
        self.parent = parent
        self.db_repo = db_repo
        self.cliente_seleccionado = Cliente()
        self.codigo = ""
        self.usuario = usuario
        self.pack()
        self.build_ui()

    def build_ui(self):
        self.btn_cliente = tk.Button(self, text="Cliente", command=self.buscar_cliente)
        self.btn_cliente.grid(row=0, column=0, columnspan=6, padx=10, pady=5)
        self.entry_cantidad = tk.Entry(self, width=5)
        self.entry_cantidad.grid(row=1, column=0, padx=10, pady=5)
        self.entry_cantidad.insert(0, "1")
        self.btn_less = tk.Button(self, text="-", width=6, command=self.decrementar_cantidad)
        self.btn_less.grid(row=1, column=1, padx=10, pady=5)
        self.btn_more = tk.Button(self, text="+", width=6, command=self.incrementar_cantidad)
        self.btn_more.grid(row=1, column=2, padx=10, pady=5)
        self.label_codigo = tk.Label(self)
        self.label_codigo.grid(row=1, column=3, padx=10, pady=5)
        self.entry_codigo = tk.Entry(self, width=30)
        self.entry_codigo.grid(row=1, column=4, padx=10, pady=5)
        self.btn_buscar_producto = tk.Button(self, text="🔍︎", command= lambda : self.buscar_producto(None))
        self.btn_buscar_producto.grid(row=1, column=5, padx=10, pady=5)
        self.btn_rm_item = tk.Button(self, text="X", command=self.delete_item)
        self.btn_rm_item.grid(row=1, column=6, padx=10, pady=5)

        self.tree_productos = ttk.Treeview(self, columns=("Codigo", "Descripcion", "Precio", "Cantidad"), show="headings", height=15)
        self.tree_productos.heading("Codigo", text="Codigo")
        self.tree_productos.heading("Descripcion", text="Descripcion")
        self.tree_productos.heading("Precio", text="Precio")
        self.tree_productos.heading("Cantidad", text="Cantidad")
        self.tree_productos.grid(row=2, column=0, columnspan=7, padx=10, pady=5)
        self.label_total = tk.Label(self, text="Total: ")
        self.label_total.grid(row=3, column=6, padx=10, pady=5)
        self.btn_pagar = tk.Button(self, text="Pagar", command= lambda : self.pay(None))
        self.btn_pagar.grid(row=4, column=0, columnspan=7,padx=10, pady=5)
        self.btn_pagar.bind("<F12>", self.pay)
        self.entry_codigo.focus_set()
    
    def buscar_cliente(self):
        ventana_buscar_cliente = BuscarClienteToplevel(self, self.db_repo)
        ventana_buscar_cliente.grab_set()
        self.wait_window(ventana_buscar_cliente)
        self.entry_codigo.focus_set()

    def incrementar_cantidad(self):
        selected = self.tree_productos.selection()
        if selected:
            self.tree_productos.item(selected, values=(self.tree_productos.item(selected)["values"][0], self.tree_productos.item(selected)["values"][1], self.tree_productos.item(selected)["values"][2], int(self.tree_productos.item(selected)["values"][3])+1))
            self.label_total.config(text="Total: $"+str(self.get_total()))
            return
        cantidad = int(self.entry_cantidad.get())
        cantidad += 1
        self.entry_cantidad.delete(0, tk.END)
        self.entry_cantidad.insert(0, str(cantidad))

    def decrementar_cantidad(self):
        selected = self.tree_productos.selection()
        if selected:
            if int(self.tree_productos.item(selected)["values"][3]) > 1:
                self.tree_productos.item(selected, values=(self.tree_productos.item(selected)["values"][0], self.tree_productos.item(selected)["values"][1], self.tree_productos.item(selected)["values"][2], int(self.tree_productos.item(selected)["values"][3])+1))
                self.label_total.config(text="Total: $"+str(self.get_total()))
            else:
                self.tree_productos.delete(selected)
                self.label_total.config(text="Total: $"+str(self.get_total()))
            return
        cantidad = int(self.entry_cantidad.get())
        if cantidad > 1:
            cantidad -= 1
            self.entry_cantidad.delete(0, tk.END)
            self.entry_cantidad.insert(0, str(cantidad))

    def buscar_producto(self, event):
        codigo = self.entry_codigo.get()

        if codigo == "":
            buscar_producto = BuscarProductoTopLevel(self, self.db_repo)
            buscar_producto.grab_set()
            self.wait_window(buscar_producto)
        else:
            self.codigo = codigo

        producto = self.db_repo.search_producto(self.codigo)
        if producto:
            #if product already in treeview, update quantity
            for child in self.tree_productos.get_children():
                if self.tree_productos.item(child)["values"][1] == producto.descripcion:
                    self.tree_productos.item(child, values=(producto.codigo, producto.descripcion, producto.precio, int(self.tree_productos.item(child)["values"][2])+1))
                    self.entry_codigo.delete(0, tk.END)
                    self.get_total()
                    self.label_total.config(text="Total: $"+str(self.get_total()))
                    self.entry_codigo.focus_set()
                    return
            self.tree_productos.insert("", tk.END, values=(producto.codigo, producto.descripcion, producto.precio, self.entry_cantidad.get()))
            self.entry_codigo.delete(0, tk.END)

            total = self.get_total()
                
            self.label_total.config(text="Total: $"+str(total))
            self.entry_codigo.focus_set()
        else:
            messagebox.showerror("Error", "Producto no encontrado")
            self.entry_codigo.delete(0, tk.END)
            self.entry_codigo.focus_set()
        self.entry_cantidad.delete(0, tk.END)
        self.entry_cantidad.insert(0, "1")
        self.entry_codigo.focus_set()
    
    def add_cuantity(self):
        #if product is selected, update quantity
        selected = self.tree_productos.selection()
        if selected:
            self.tree_productos.item(selected, values=(self.tree_productos.item(selected)["values"][0], self.tree_productos.item(selected)["values"][1], self.tree_productos.item(selected)["values"][2], int(self.tree_productos.item(selected)["values"][3])+1))
            self.label_total.config(text="Total: $"+str(self.get_total()))
        else:
            #icrement entry_cuantity
            cuantity = int(self.entry_cantidad.get())
            cuantity += 1
            self.entry_cantidad.delete(0, tk.END)
            self.entry_cantidad.insert(0, str(cuantity))

    def delete_item(self):
        selected = self.tree_productos.selection()
        if selected:
            self.tree_productos.delete(selected)
            self.label_total.config(text="Total: $"+str(self.get_total()))
        else:
            messagebox.showerror("Error", "Seleccione un producto")

    def get_total(self):
        total = 0
        for child in self.tree_productos.get_children():
            total += float(self.tree_productos.item(child)["values"][2]) * int(self.tree_productos.item(child)["values"][3])
        return total
    
    def pay(self, event):
        try:
            #validate that there are products
            if not self.tree_productos.get_children():
                messagebox.showerror("Error", "Agregue productos a la venta")
                self.entry_codigo.focus_set()
                return
            #validate cliente
            if self.cliente_seleccionado.id == 0:
                messagebox.showerror("Error", "Seleccione un cliente")
                self.buscar_cliente()
                return
            #validate stock for each product
            for child in self.tree_productos.get_children():
                producto = self.db_repo.search_producto(self.tree_productos.item(child)["values"][0])
                if producto.stock < float(self.tree_productos.item(child)["values"][3]):
                    messagebox.showerror("Error", "No hay suficiente stock para el producto "+producto.descripcion)
                    return
            #create a new venta
            id_venta = self.db_repo.create_venta(self.cliente_seleccionado.id, self.usuario.id, self.get_total())

            #create a new detalle_venta
            for child in self.tree_productos.get_children():
                producto = self.db_repo.search_producto(self.tree_productos.item(child)["values"][0])
                self.db_repo.create_detalle_venta(id_venta, producto.id, int(self.tree_productos.item(child)["values"][3]))
                self.db_repo.update_producto(producto.codigo, producto.descripcion, producto.precio, producto.stock - Decimal(self.tree_productos.item(child)["values"][3]))
            
            #update cliente points
            puntos_ganados = self.db_repo.update_cliente_points(self.cliente_seleccionado.id, self.get_total())
            
            messagebox.showinfo("Éxito", f"Venta concretada + {puntos_ganados} puntos para {self.cliente_seleccionado.nombre}")
            self.tree_productos.delete(*self.tree_productos.get_children())
            self.label_total.config(text="Total: $0.00")
            self.entry_codigo.delete(0, tk.END)
            self.entry_codigo.focus_set()
            self.cliente_seleccionado = Cliente()
            self.btn_cliente.config(text="Cliente")
        except Exception as e:
            messagebox.showerror("Error", str(e))
