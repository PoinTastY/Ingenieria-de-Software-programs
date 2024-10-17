import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from Interface.db_repo import DbRepo

class VentaTab(tk.Frame):
    def __init__(self, parent, db_repo : DbRepo):
        super().__init__(parent)
        self.parent = parent
        self.db_repo = db_repo
        self.pack()
        self.build_ui()

    def build_ui(self):
        self.btn_cliente = tk.Button(self, text="Cliente")
        self.btn_cliente.grid(row=0, column=0, columnspan=6, padx=10, pady=5)
        self.entry_cantidad = tk.Entry(self, width=5)
        self.entry_cantidad.grid(row=1, column=0, padx=10, pady=5)
        self.entry_cantidad.insert(0, "1")
        self.btn_less = tk.Button(self, text="-", width=6)
        self.btn_less.grid(row=1, column=1, padx=10, pady=5)
        self.btn_more = tk.Button(self, text="+", width=6)
        self.btn_more.grid(row=1, column=2, padx=10, pady=5)
        self.label_codigo = tk.Label(self)
        self.label_codigo.grid(row=1, column=3, padx=10, pady=5)
        self.entry_codigo = tk.Entry(self, width=30)
        self.entry_codigo.grid(row=1, column=4, padx=10, pady=5)
        self.btn_buscar_producto = tk.Button(self, text="🔍︎", command=self.buscar_producto)
        self.btn_buscar_producto.grid(row=1, column=5, padx=10, pady=5)
        self.btn_rm_item = tk.Button(self, text="X", command=self.delete_item)
        self.btn_rm_item.grid(row=1, column=6, padx=10, pady=5)

        self.tree_productos = ttk.Treeview(self, columns=("Descripcion", "Precio", "Cantidad"), show="headings", height=15)
        self.tree_productos.heading("Descripcion", text="Descripcion")
        self.tree_productos.heading("Precio", text="Precio")
        self.tree_productos.heading("Cantidad", text="Cantidad")
        self.tree_productos.grid(row=2, column=0, columnspan=7, padx=10, pady=5)
        self.label_total = tk.Label(self, text="Total: ")
        self.label_total.grid(row=3, column=6, padx=10, pady=5)
        self.btn_pagar = tk.Button(self, text="Pagar", command=self.pay)
        self.btn_pagar.grid(row=4, column=0, columnspan=7,padx=10, pady=5)
        self.btn_pagar.bind("<F12>", self.pay)
        self.entry_codigo.focus_set()
    
    def buscar_producto(self, event):
        codigo = self.entry_codigo.get()
        producto = self.db_repo.search_producto(codigo)
        if producto:
            #if product already in treeview, update quantity
            for child in self.tree_productos.get_children():
                if self.tree_productos.item(child)["values"][0] == producto.descripcion:
                    self.tree_productos.item(child, values=(producto.descripcion, producto.precio, int(self.tree_productos.item(child)["values"][2])+1))
                    self.entry_codigo.delete(0, tk.END)
                    self.get_total()
                    self.label_total.config(text="Total: $"+str(self.get_total()))
                    self.entry_codigo.focus_set()
                    return
            self.tree_productos.insert("", tk.END, values=(producto.descripcion, producto.precio, self.entry_cantidad.get()))
            self.entry_codigo.delete(0, tk.END)
            7501557140490

            total = self.get_total()
                
            self.label_total.config(text="Total: $"+str(total))
            self.entry_codigo.focus_set()
        else:
            messagebox.showerror("Error", "Producto no encontrado")
            self.entry_codigo.delete(0, tk.END)
            self.entry_codigo.focus_set()
        self.entry_cantidad.delete(0, tk.END)
        self.entry_cantidad.insert(0, "1")
    
    def add_cuantity(self):
        #if product is selected, update quantity
        selected = self.tree_productos.selection()
        if selected:
            self.tree_productos.item(selected, values=(self.tree_productos.item(selected)["values"][0], self.tree_productos.item(selected)["values"][1], int(self.tree_productos.item(selected)["values"][2])+1))
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

    def pay(self, event):
        pass

    def get_total(self):
        total = 0
        for child in self.tree_productos.get_children():
            total += float(self.tree_productos.item(child)["values"][1]) * int(self.tree_productos.item(child)["values"][2])
        return total
