from tkinter import messagebox
import tkinter as tk

from Data.db_repo import DBRepo
from Presentation.usuarios import Usuarios
from Presentation.clientes import Clientes
from Presentation.autos import Autos
from Presentation.partes import Partes
from Presentation.reparaciones import Reparaciones

from Domain.Entities.usuario import Usuario

class MainPage(tk.Tk):
    def __init__(self, db_repo : DBRepo, user : Usuario, login):
        super().__init__()
        self.db_repo = db_repo
        self.user = user
        self.title("Taller Mecanico")
        self.geometry("300x300")

        self.login = login

        self.build_mainpage()
        self.view_instance = None


    def build_mainpage(self):
        self.botones_frame = tk.Frame(self)
        self.botones_frame.pack(fill=tk.Y)

        self.btn_usuarios = tk.Button(self.botones_frame, text="Usuarios", command=self.ventana_usuarios)
        self.btn_usuarios.pack(pady=10, padx=20)

        self.btn_clientes = tk.Button(self.botones_frame, text="Clientes", command=self.ventana_clientes)
        self.btn_clientes.pack(pady=10, padx=20)
        

        self.btn_autos = tk.Button(self.botones_frame, text="Autos", command=self.ventana_autos)
        self.btn_autos.pack(pady=10, padx=20)

        self.btn_reparaciones = tk.Button(self.botones_frame, text="Reparaciones", command=self.ventana_reparaciones)
        self.btn_reparaciones.pack(pady=10, padx=20)

        self.btn_partes = tk.Button(self.botones_frame, text="Partes", command=self.ventana_partes)
        self.btn_partes.pack(pady=10, padx=20)

        self.btn_salir = tk.Button(self.botones_frame, text="Salir", command=self.quit)
        self.btn_salir.pack(pady=10, padx=20)

        self.update_user()

    def quit(self) -> None:
        self.destroy()
        self.login.deiconify()
        
    def update_user(self):
        if(self.user.perfil != "Admin"):
            if(self.user.perfil == "Secretaria"):
                self.btn_usuarios.config(state=tk.DISABLED)
                self.btn_clientes.config(state=tk.NORMAL)
                self.btn_autos.config(state=tk.NORMAL)
                self.btn_partes.config(state=tk.DISABLED)
                self.btn_reparaciones.config(state=tk.DISABLED)

            elif(self.user.perfil == "Mecanico"):
                self.btn_usuarios.config(state=tk.DISABLED)
                self.btn_clientes.config(state=tk.DISABLED)
                self.btn_autos.config(state=tk.DISABLED)
                self.btn_reparaciones.config(state=tk.NORMAL)
                self.btn_partes.config(state=tk.DISABLED)

        else:
            self.btn_usuarios.config(state=tk.NORMAL)
            self.btn_clientes.config(state=tk.NORMAL)
            self.btn_autos.config(state=tk.NORMAL)
            self.btn_partes.config(state=tk.NORMAL)
            self.btn_reparaciones.config(state=tk.NORMAL)


    def ventana_usuarios(self):
        self.withdraw()
        self.open_view(Usuarios)

    def ventana_clientes(self):
        self.withdraw()
        self.open_view(Clientes)

    def ventana_autos(self):
        self.withdraw()
        self.open_view(Autos)

    def ventana_reparaciones(self):
        self.withdraw()
        self.open_view(Reparaciones)

    def ventana_partes(self):
        self.withdraw()
        self.open_view(Partes)

    def open_view(self, view_class):
        
        self.view_instance = view_class(self.db_repo, self, self.user)
        self.view_instance.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.view_instance.destroy()
        self.deiconify()