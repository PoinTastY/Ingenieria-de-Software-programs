import tkinter as tk
from tkinter import messagebox

from Presentation.main_page import MainPage
from Data.db_repo import DBRepo

class Login(tk.Tk):
    def __init__(self, db_repo : DBRepo):
        super().__init__()
        self.db_repo = db_repo
        self.title("Login")
        self.geometry("400x400")  # Ajustar tamaño

        tk.Label(self, text="Usuario:").pack(padx=10, pady=5)
        self.entry_usuario = tk.Entry(self)
        self.entry_usuario.pack(padx=10, pady=5)

        tk.Label(self, text="Contraseña:").pack(padx=10, pady=5)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack(padx=10, pady=5)

        self.btn_ingresar = tk.Button(self, text="Ingresar", command=self.iniciar_sesion)
        self.btn_ingresar.pack(pady=10)

    def iniciar_sesion(self):
        try:

            user = self.entry_usuario.get()
            password = self.entry_password.get()

            appuser = self.db_repo.login(user, password)
            if(appuser):
                self.withdraw()
                mainpage = MainPage(self.db_repo, appuser)
                mainpage.mainloop()
                print("mainpage closed")

            else:
                self.entry_usuario.delete(0, tk.END)
                self.entry_password.delete(0, tk.END)
                messagebox.showerror("Error", "Usuario o contraseña incorrecta.")

        except Exception as e:
            messagebox.showerror("Error", "Usuario o contraseña incorrecta. ({})".format(e))
        