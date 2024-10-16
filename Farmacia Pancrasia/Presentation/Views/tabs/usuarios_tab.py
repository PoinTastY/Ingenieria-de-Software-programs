import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from Interface.db_repo import DbRepo

class UsuariosTab(tk.Frame):
    def __init__(self, parent, db_repo : DbRepo):
        super().__init__(parent)
        self.parent = parent
        self.db_repo = db_repo
        self.pack()
        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="Buscar usuario:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_buscar_usuario = tk.Entry(self, state=tk.NORMAL)
        self.entry_buscar_usuario.grid(row=0, column=1, padx=10, pady=10)
        self.btn_buscar = tk.Button(self, text="Buscar", command=lambda: self.buscar_usuario(self.entry_buscar_usuario.get()))
        self.btn_buscar.grid(row=0, column=2, padx=10, pady=10)

        tk.Label(self, text="ID Usuario:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_id_usuario = tk.Entry(self, state=tk.DISABLED)
        self.entry_id_usuario.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self, text="Nombre de Usuario:").grid(row=3, column=0, padx=10, pady=10)
        self.entry_nombre_usuario = tk.Entry(self, state=tk.DISABLED)
        self.entry_nombre_usuario.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(self, text="Contraseña:").grid(row=4, column=0, padx=10, pady=10)
        self.entry_contraseña = tk.Entry(self, show="*", state=tk.DISABLED)
        self.entry_contraseña.grid(row=4, column=1, padx=10, pady=10)

        tk.Label(self, text="Perfil:").grid(row=5, column=0, padx=10, pady=10)
        self.combo_perfil = ttk.Combobox(self, values=["Admin", "Secretaria", "Mecanico"], state=tk.DISABLED)
        self.combo_perfil.grid(row=5, column=1, padx=10, pady=10)

        self.btn_nuevo = tk.Button(self, text="Nuevo", command=self.nuevo_usuario)
        self.btn_nuevo.grid(row=6, column=0, padx=10, pady=10)

        self.btn_guardar = tk.Button(self, text="Guardar", state=tk.DISABLED, command=self.guardar_usuario)
        self.btn_guardar.grid(row=6, column=1, padx=10, pady=10)

        self.btn_editar = tk.Button(self, text="Editar", state=tk.DISABLED, command=self.editar_usuario)
        self.btn_editar.grid(row=6, column=3, padx=10, pady=10)
    
        self.btn_borrar = tk.Button(self, text="Borrar", state=tk.DISABLED, command=self.borrar_usuario)
        self.btn_borrar.grid(row=7, column=0, padx=10, pady=10)

    def borrar_usuario(self):
        try:
            id = self.entry_id_usuario.get()
            self.db_repo.borrar_usuario(id)
            messagebox.showinfo("Exito", f"Se borro al usuario con id: {id}")
        except Exception as e:
            messagebox.showerror("Error", "Error eliminando usuario: {}".format(e))
        finally:
            self.habilitar_campos(self.entry_id_usuario, self.entry_nombre_usuario, self.entry_contraseña, self.btn_nuevo)
            self.limpiar_campos(self.entry_id_usuario, self.entry_nombre_usuario, self.entry_contraseña)
            self.combo_perfil.set("")
            self.deshabilitar_campos(self.entry_id_usuario, self.entry_nombre_usuario, self.entry_contraseña, self.btn_borrar, self.btn_editar, self.btn_guardar)

    def nuevo_usuario(self):
        try:
            self.limpiar_campos(self.entry_id_usuario, self.entry_nombre_usuario, self.entry_contraseña)
            self.habilitar_campos(self.entry_id_usuario, self.entry_nombre_usuario, self.entry_contraseña, self.combo_perfil, self.btn_guardar)
            self.entry_id_usuario.insert(0, self.db_repo.obtener_siguiente_id_usuario())
            self.deshabilitar_campos(self.entry_id_usuario, self.btn_nuevo, self.btn_editar)
        except Exception as e:
            messagebox.showerror("Error", "Error al obtener siguiente ID. ({})".format(e))

    def limpiar_campos(self, *campos):
        for campo in campos:
            campo.delete(0, tk.END)

    def habilitar_campos(self, *campos):
        for campo in campos:
            campo.config(state=tk.NORMAL)
    
    def deshabilitar_campos(self, *campos):
        for campo in campos:
            campo.config(state=tk.DISABLED)

    def buscar_usuario(self, nombre):
        try:
            usuario = self.db_repo.buscar_usuario(nombre=nombre)
            if usuario:
                self.habilitar_campos(self.entry_id_usuario, self.entry_nombre_usuario, self.entry_contraseña, self.combo_perfil)
                self.limpiar_campos(self.entry_buscar_usuario, self.entry_id_usuario, self.entry_nombre_usuario, self.entry_contraseña)
                self.entry_id_usuario.insert(0, usuario.id)
                self.entry_nombre_usuario.insert(0, usuario.nombre)
                self.entry_contraseña.insert(0, usuario.password)
                self.combo_perfil.set(usuario.perfil)
                self.deshabilitar_campos(self.entry_id_usuario, self.entry_nombre_usuario, self.entry_contraseña, self.combo_perfil,
                                         self.btn_guardar, self.btn_nuevo)
                self.habilitar_campos(self.btn_editar, self.btn_borrar)

            else:
                messagebox.showinfo("Información", "Usuario no encontrado")
        except Exception as e:
            messagebox.showerror("Error", "Error al buscar usuario. ({})".format(e))

    def guardar_usuario(self):
        id_usuario = self.entry_id_usuario.get()
        user_name = self.entry_nombre_usuario.get()
        password = self.entry_contraseña.get()
        perfil = self.combo_perfil.get()
        try:
            self.db_repo.create_usuario(nombre=user_name, password=password, perfil=perfil)
            messagebox.showinfo("Información", "Usuario guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", "Error al guardar usuario. ({})".format(e))
        finally:
            self.habilitar_campos(self.btn_borrar)
    
    def editar_usuario(self):
        self.habilitar_campos(self.entry_nombre_usuario, self.entry_contraseña, self.combo_perfil, self.btn_guardar)
        self.deshabilitar_campos(self.btn_editar, self.btn_nuevo, self.entry_id_usuario)
        self.entry_nombre_usuario.focus_set()
