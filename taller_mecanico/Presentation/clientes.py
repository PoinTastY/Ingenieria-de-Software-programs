import tkinter as tk

from Data.db_repo import DBRepo
from Domain.Entities.usuario import Usuario

class Clientes(tk.Tk):
    def __init__(self, db_repo : DBRepo, main_page, user : Usuario):
        super().__init__()
        self.db_repo = db_repo
        self.title("Clientes")
        self.geometry("400x400")
