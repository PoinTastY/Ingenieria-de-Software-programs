from tkinter import messagebox
import tkinter as tk

from Data.db_repo import DBRepo

class Partes(tk.Tk):
    def __init__(self, db_repo: DBRepo, main_page, user):
        super().__init__()
        self.db_repo = db_repo
        self.mainwindow = main_page
        self.user = user
        self.title("Partes")
        self.geometry("550x220")
        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="Ingrese ID de parte a buscar:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_buscar_id = tk.Entry(self)
        self.entry_buscar_id.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self, text="Buscar", command=lambda: self.buscar_parte(self.entry_buscar_id.get())).grid(row=0, column=2, padx=10, pady=10)

        tk.Label(self, text="ID:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_id_parte = tk.Entry(self, state=tk.DISABLED)
        self.entry_id_parte.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self, text="Nombre:").grid(row=2, column=0, padx=10, pady=10)
        self.entry_nombre = tk.Entry(self, state=tk.DISABLED)
        self.entry_nombre.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self, text="Costo:").grid(row=3, column=0, padx=10, pady=10)
        self.entry_costo = tk.Entry(self, state=tk.DISABLED)
        self.entry_costo.grid(row=3, column=1, padx=10, pady=10)

        self.btn_nuevo = tk.Button(self, text="Nuevo", command=self.nuevo_parte)
        self.btn_nuevo.grid(row=4, column=0, padx=10, pady=10)

        self.btn_guardar = tk.Button(self, text="Guardar", state=tk.DISABLED, command=lambda: self.guardar_parte(self.entry_id_parte.get(), self.entry_nombre.get(), self.entry_costo.get()))
        self.btn_guardar.grid(row=4, column=1, padx=10, pady=10)

        self.btn_cancelar = tk.Button(self, text="Cancelar", command=self.cancelar)
        self.btn_cancelar.grid(row=4, column=2, padx=10, pady=10)

        self.btn_editar = tk.Button(self, state=tk.DISABLED, text="Editar", command=self.editar_parte)
        self.btn_editar.grid(row=4, column=3, padx=10, pady=10)

        self.btn_eliminar = tk.Button(self, state=tk.DISABLED, text="Eliminar", command=self.eliminar_parte)
        self.btn_eliminar.grid(row=4, column=4, padx=10, pady=10)

    def cancelar(self):
        self.destroy()
        self.mainwindow.deiconify()

    def limpiar_campos(self, *campos):
        for campo in campos:
            campo.delete(0, tk.END)

    def habilitar_deshabilitar_campos(self, *campos, state):
        for campo in campos:
            campo.config(state=state)

    def buscar_parte(self, id_parte):
        try:
            parte = self.db_repo.buscar_parte(id_parte)
            if parte:
                self.habilitar_deshabilitar_campos(self.entry_id_parte, self.entry_nombre,
                                                    self.entry_costo, self.btn_editar, state=tk.NORMAL)
                self.entry_id_parte.insert(0, parte.id)
                self.entry_nombre.insert(0, parte.nombre)
                self.entry_costo.insert(0, parte.costo)

                self.habilitar_deshabilitar_campos(self.entry_id_parte, state=tk.DISABLED)
                self.habilitar_deshabilitar_campos(self.btn_eliminar, state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", "Error al buscar parte. ({})".format(e))

    def eliminar_parte(self):
        try:
            self.db_repo.borrar_parte(self.entry_id_parte.get())
            messagebox.showinfo("Parte eliminada", "Parte eliminada correctamente")
            self.limpiar_campos(self.entry_id_parte, self.entry_nombre, self.entry_costo)
            self.habilitar_deshabilitar_campos(self.entry_id_parte, self.entry_nombre, self.entry_costo, self.btn_editar, self.btn_eliminar, state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", "Error al eliminar parte. ({})".format(e))

    def editar_parte(self):
        self.habilitar_deshabilitar_campos(self.entry_nombre, self.entry_costo, self.btn_guardar, self.btn_eliminar, state=tk.NORMAL)
        self.habilitar_deshabilitar_campos(self.btn_nuevo, self.entry_id_parte, state=tk.DISABLED)

    def nuevo_parte(self):
        self.habilitar_deshabilitar_campos(self.entry_id_parte, self.entry_nombre, self.entry_costo, self.btn_guardar, state=tk.NORMAL)
        self.entry_id_parte.delete(0, tk.END)
        self.entry_id_parte.insert(0, self.db_repo.obtener_siguiente_id_partes())
        self.habilitar_deshabilitar_campos(self.btn_nuevo, self.entry_id_parte, self.btn_eliminar, state=tk.DISABLED)

    def guardar_parte(self, id, nombre, costo):
        try:
            # validar si costo es un número
            try:
                float(costo)
            except:
                messagebox.showerror("Error", "El costo debe ser un número")
                return
            self.db_repo.guardar_parte(id_parte=id, nombre=nombre, costo=costo)
            messagebox.showinfo("Parte guardada", "Parte guardada correctamente")
            self.habilitar_deshabilitar_campos(self.btn_nuevo, self.entry_id_parte, state=tk.NORMAL)
            self.limpiar_campos(self.entry_id_parte, self.entry_nombre, self.entry_costo)
            self.habilitar_deshabilitar_campos(self.entry_id_parte, self.entry_nombre, self.entry_costo, self.btn_guardar, state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", "Error al guardar parte. ({})".format(e))
