import tkinter as tk
from tkinter import ttk, messagebox
#import psycopg2

#def conectar_db():


def login():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    if usuario == "1" and contraseña == "1":
        ventana_principal()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrecta")

def ventana_principal():
    ventana_login.withdraw()
    ventana_opciones = tk.Toplevel()
    ventana_opciones.title("Opciones")
    ventana_opciones.geometry("400x400")  # Ajustar el tamaño

    botones_frame = tk.Frame(ventana_opciones)
    botones_frame.pack(side=tk.LEFT, fill=tk.Y)

    btn_usuarios = tk.Button(botones_frame, text="Usuarios", command=ventana_usuarios)
    btn_usuarios.pack(pady=10)
    tk.Button(botones_frame, text="Clientes").pack(pady=10)
    tk.Button(botones_frame, text="Partes").pack(pady=10)
    tk.Button(botones_frame, text="Autos").pack(pady=10)
    tk.Button(botones_frame, text="Salir", command=ventana_opciones.destroy).pack(pady=10)

def ventana_usuarios():
    ventana_busqueda = tk.Toplevel()
    ventana_busqueda.title("Gestión de Usuarios")
    ventana_busqueda.geometry("450x400")  # Tamaño para mantener consistencia

    tk.Label(ventana_busqueda, text="Buscar por ID:").grid(row=0, column=0, padx=10, pady=10)
    entry_buscar_id = tk.Entry(ventana_busqueda)
    entry_buscar_id.grid(row=0, column=1, padx=10, pady=10)
    tk.Button(ventana_busqueda, text="Buscar", command=lambda: buscar_usuario(entry_buscar_id.get())).grid(row=0, column=2, padx=10, pady=10)

    tk.Label(ventana_busqueda, text="ID Usuario:").grid(row=1, column=0, padx=10, pady=10)
    entry_id_usuario = tk.Entry(ventana_busqueda)
    entry_id_usuario.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(ventana_busqueda, text="Nombre:").grid(row=2, column=0, padx=10, pady=10)
    entry_nombre = tk.Entry(ventana_busqueda)
    entry_nombre.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(ventana_busqueda, text="Nombre de Usuario:").grid(row=3, column=0, padx=10, pady=10)
    entry_nombre_usuario = tk.Entry(ventana_busqueda)
    entry_nombre_usuario.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(ventana_busqueda, text="Contraseña:").grid(row=4, column=0, padx=10, pady=10)
    entry_contraseña = tk.Entry(ventana_busqueda, show="*")
    entry_contraseña.grid(row=4, column=1, padx=10, pady=10)

    tk.Label(ventana_busqueda, text="Perfil:").grid(row=5, column=0, padx=10, pady=10)
    combo_perfil = ttk.Combobox(ventana_busqueda, values=["Admin", "Secretaria", "Mecanico"])
    combo_perfil.grid(row=5, column=1, padx=10, pady=10)

    btn_nuevo = tk.Button(ventana_busqueda, text="Nuevo", command=lambda: limpiar_campos(entry_id_usuario, entry_nombre, entry_nombre_usuario, entry_contraseña, combo_perfil))
    btn_nuevo.grid(row=6, column=0, padx=10, pady=10)

    btn_guardar = tk.Button(ventana_busqueda, text="Guardar", command=lambda: guardar_usuario(entry_id_usuario.get(), entry_nombre.get(), entry_nombre_usuario.get(), entry_contraseña.get(), combo_perfil.get()))
    btn_guardar.grid(row=6, column=1, padx=10, pady=10)

    btn_cancelar = tk.Button(ventana_busqueda, text="Cancelar", command=ventana_busqueda.destroy)
    btn_cancelar.grid(row=6, column=2, padx=10, pady=10)

    btn_editar = tk.Button(ventana_busqueda, text="Editar")
    btn_editar.grid(row=6, column=3, padx=10, pady=10)

def limpiar_campos(*campos):
    for campo in campos:
        campo.delete(0, tk.END)

def buscar_usuario(id_usuario):
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id_usuario,))
        usuario = cursor.fetchone()
        if usuario:
            messagebox.showinfo("Usuario Encontrado", f"Usuario: {usuario}")
        else:
            messagebox.showerror("Error", "Usuario no encontrado")
        conexion.close()

def guardar_usuario(id_usuario, nombre, nombre_usuario, contraseña, perfil):
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (id, nombre, nombre_usuario, contraseña, perfil) VALUES (%s, %s, %s, %s, %s)", (id_usuario, nombre, nombre_usuario, contraseña, perfil))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Usuario guardado correctamente")

ventana_login = tk.Tk()
ventana_login.title("Login")
ventana_login.geometry("400x400")  # Ajustar tamaño

tk.Label(ventana_login, text="Usuario:").pack(padx=10, pady=5)
entry_usuario = tk.Entry(ventana_login)
entry_usuario.pack(padx=10, pady=5)

tk.Label(ventana_login, text="Contraseña:").pack(padx=10, pady=5)
entry_contraseña = tk.Entry(ventana_login, show="*")
entry_contraseña.pack(padx=10, pady=5)

tk.Button(ventana_login, text="Ingresar", command=login).pack(pady=10)

ventana_login.mainloop()