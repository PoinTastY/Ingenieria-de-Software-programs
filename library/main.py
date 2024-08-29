import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

libros = []
last_id = 1

def nuevo(): 
    global last_id

    limpiar_campos()

    # enable disable stuff
    entry_titulo.config(state=tk.NORMAL)
    entry_autor.config(state=tk.NORMAL)
    entry_editorial.config(state=tk.NORMAL)
    combo_clasificacion.config(state=tk.NORMAL)

    btn_nuevo.config(state=tk.DISABLED)
    btn_editar.config(state=tk.DISABLED)
    btn_eliminar.config(state=tk.DISABLED)
    btn_guardar.config(state=tk.NORMAL)
    btn_cancelar.config(state=tk.NORMAL)
    
    entry_id.config(state=tk.NORMAL)
    entry_id.delete(0, tk.END)
    entry_id.insert(0, str(last_id))
    entry_id.config(state=tk.DISABLED)


def guardar():
    global last_id

    id_libro = entry_id.get()
    titulo = entry_titulo.get()
    autor = entry_autor.get()
    editorial = entry_editorial.get()
    clasificacion = combo_clasificacion.get()

    libro_existente = None
    for libro in libros:
        if libro["ID"] == id_libro: 
            libro_existente = libro
            break

    if libro_existente:
        # if exist, we update
        libro_existente["Título"] = titulo
        libro_existente["Autor"] = autor
        libro_existente["Editorial"] = editorial
        libro_existente["Clasificación"] = clasificacion
        print(f"Libro actualizado: {libro_existente}")
    else:
        # if not exist, we create
        nuevo_libro = {
            "ID": id_libro,
            "Título": titulo,
            "Autor": autor,
            "Editorial": editorial,
            "Clasificación": clasificacion
        }
        libros.append(nuevo_libro)
        print(f"Libro guardado: {nuevo_libro}")
        #update global index variable
        last_id += 1

    # update ui
    btn_nuevo.config(state=tk.NORMAL)
    btn_editar.config(state=tk.DISABLED)
    btn_eliminar.config(state=tk.DISABLED)
    btn_guardar.config(state=tk.DISABLED)
    btn_cancelar.config(state=tk.DISABLED)

    limpiar_campos()

def buscar():
    id_busqueda = entry_search.get()
    
    if not id_busqueda.isdigit():
        messagebox.showerror("Error", "Por favor, ingrese un ID válido.")
        limpiar_campos()
        return

    # find by id
    libro_encontrado = None
    for libro in libros:
        if libro["ID"] == id_busqueda:
            libro_encontrado = libro
            break

    if libro_encontrado:
        #display match
        entry_id.config(state=tk.NORMAL)
        entry_id.delete(0, tk.END)
        entry_id.insert(0, libro_encontrado["ID"])
        entry_id.config(state=tk.DISABLED)

        entry_titulo.config(state=tk.NORMAL)
        entry_titulo.delete(0, tk.END)
        entry_titulo.insert(0, libro_encontrado["Título"])
        entry_titulo.config(state=tk.DISABLED)

        entry_autor.config(state=tk.NORMAL)
        entry_autor.delete(0, tk.END)
        entry_autor.insert(0, libro_encontrado["Autor"])
        entry_autor.config(state=tk.DISABLED)

        entry_editorial.config(state=tk.NORMAL)
        entry_editorial.delete(0, tk.END)
        entry_editorial.insert(0, libro_encontrado["Editorial"])
        entry_editorial.config(state=tk.DISABLED)

        combo_clasificacion.config(state=tk.NORMAL)
        combo_clasificacion.set(libro_encontrado["Clasificación"])
        combo_clasificacion.config(state=tk.DISABLED)

        # enable edit or delete
        btn_editar.config(state=tk.NORMAL)
        btn_eliminar.config(state=tk.NORMAL)
    else:
        # show not found
        messagebox.showinfo("Información", f"No se encontró ningún libro con ID {id_busqueda}")
        limpiar_campos()

def editar():
    #enable/disable entries
    entry_titulo.config(state=tk.NORMAL)
    entry_autor.config(state=tk.NORMAL)
    entry_editorial.config(state=tk.NORMAL)
    combo_clasificacion.config(state=tk.NORMAL)
    
    btn_guardar.config(state=tk.NORMAL)
    btn_cancelar.config(state=tk.NORMAL)

    btn_editar.config(state=tk.DISABLED)
    btn_eliminar.config(state=tk.DISABLED)
    btn_nuevo.config(state=tk.DISABLED)

def eliminar():
     # confirm elimination
    respuesta = messagebox.askyesno("Confirmar eliminación", f"¿Está seguro de eliminar el libro con ID {entry_id.get()}?")
    
    if respuesta:
        for libro in libros:
            if libro["ID"] == entry_id.get():
                libros.remove(libro)
                print(f"Libro eliminado: {entry_titulo.get()}")  # Para verificar en consola
                break
        
        limpiar_campos()
        libro_actual = None

        #update ui
        btn_nuevo.config(state=tk.NORMAL)
        btn_editar.config(state=tk.DISABLED)
        btn_eliminar.config(state=tk.DISABLED)
        btn_guardar.config(state=tk.DISABLED)
        btn_cancelar.config(state=tk.DISABLED)

        messagebox.showinfo("Información", "Libro eliminado correctamente.")

def cancelar():
    # abort anything and restore ui
    btn_nuevo.config(state=tk.NORMAL)
    btn_editar.config(state=tk.NORMAL)
    btn_eliminar.config(state=tk.NORMAL)
    btn_guardar.config(state=tk.DISABLED)
    btn_cancelar.config(state=tk.DISABLED)

    limpiar_campos()

def limpiar_campos():
    entry_search.config(state=tk.NORMAL)
    entry_search.delete(0, tk.END)
    entry_id.config(state=tk.NORMAL)
    entry_id.delete(0, tk.END)
    entry_id.config(state=tk.DISABLED)
    entry_titulo.config(state=tk.NORMAL)
    entry_titulo.delete(0, tk.END)
    entry_autor.config(state=tk.NORMAL)
    entry_autor.delete(0, tk.END)
    entry_editorial.config(state=tk.NORMAL)
    entry_editorial.delete(0, tk.END)
    combo_clasificacion.set("")

    entry_id.config(state=tk.DISABLED)
    entry_titulo.config(state=tk.DISABLED)
    entry_autor.config(state=tk.DISABLED)
    entry_editorial.config(state=tk.DISABLED)
    combo_clasificacion.config(state=tk.DISABLED)

# main window setup
root = tk.Tk()
root.title("Sistema de Gestión de Libros")
root.geometry("400x300")

# create ui
label_search = tk.Label(root, text="Ingrese ID a buscar:")
label_search.grid(row=0, column=0, padx=10, pady=10)

entry_search = tk.Entry(root)
entry_search.grid(row=0, column=1, padx=10, pady=10)

btn_buscar = tk.Button(root, text="Buscar", command=buscar)
btn_buscar.grid(row=0, column=2, padx=10, pady=10)

label_id = tk.Label(root, text="ID:")
label_id.grid(row=1, column=0, padx=10, pady=5)

entry_id = tk.Entry(root)
entry_id.grid(row=1, column=1, padx=10, pady=5)
entry_id.config(state=tk.DISABLED)

label_titulo = tk.Label(root, text="Título:")
label_titulo.grid(row=2, column=0, padx=10, pady=5)

entry_titulo = tk.Entry(root)
entry_titulo.grid(row=2, column=1, padx=10, pady=5)
entry_titulo.config(state=tk.DISABLED)

label_autor = tk.Label(root, text="Autor:")
label_autor.grid(row=3, column=0, padx=10, pady=5)

entry_autor = tk.Entry(root)
entry_autor.grid(row=3, column=1, padx=10, pady=5)
entry_autor.config(state=tk.DISABLED)

label_editorial = tk.Label(root, text="Editorial:")
label_editorial.grid(row=4, column=0, padx=10, pady=5)

entry_editorial = tk.Entry(root)
entry_editorial.grid(row=4, column=1, padx=10, pady=5)
entry_editorial.config(state=tk.DISABLED)

label_clasificacion = tk.Label(root, text="Clasificación:")
label_clasificacion.grid(row=5, column=0, padx=10, pady=5)

combo_clasificacion = ttk.Combobox(root, values=["A", "B", "C", "D"])
combo_clasificacion.grid(row=5, column=1, padx=10, pady=5)
combo_clasificacion.config(state=tk.DISABLED)

# buttons
btn_nuevo = tk.Button(root, text="Nuevo", command=nuevo)
btn_nuevo.grid(row=6, column=0, padx=5, pady=10)

btn_guardar = tk.Button(root, text="Guardar", command=guardar)
btn_guardar.grid(row=6, column=1, padx=5, pady=10)
btn_guardar.config(state=tk.DISABLED)

btn_cancelar = tk.Button(root, text="Cancelar", command=cancelar)
btn_cancelar.grid(row=6, column=2, padx=5, pady=10)
btn_cancelar.config(state=tk.DISABLED)

btn_editar = tk.Button(root, text="Editar", command=editar)
btn_editar.grid(row=7, column=0, padx=5, pady=10)

btn_eliminar = tk.Button(root, text="Eliminar", command=eliminar)
btn_eliminar.grid(row=7, column=1, padx=5, pady=10)

root.mainloop()