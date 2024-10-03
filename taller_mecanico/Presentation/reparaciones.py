from tkinter import messagebox, simpledialog, ttk
import tkinter as tk

from tkcalendar import DateEntry

from Data.db_repo import DBRepo


class Reparaciones(tk.Tk):
    def __init__(self, db_repo: DBRepo, main_page, user):
        super().__init__()
        self.db_repo = db_repo
        self.mainwindow = main_page
        self.user = user
        self.title("Reparaciones")
        self.geometry("700x550")
        self.build_ui()

    def build_ui(self):
        # Buscar reparación
        tk.Label(self, text="Ingrese ID de reparación a buscar:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_buscar_id = tk.Entry(self)
        self.entry_buscar_id.grid(row=0, column=1, padx=10, pady=10)
        self.btn_buscar = tk.Button(self, text="Buscar", command=self.buscar_reparacion)
        self.btn_buscar.grid(row=0, column=2, padx=10, pady=10)

        # Campos de la reparación
        tk.Label(self, text="ID:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_id_reparacion = tk.Entry(self, state=tk.DISABLED)
        self.entry_id_reparacion.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self, text="ID Auto:").grid(row=2, column=0, padx=10, pady=10)
        self.entry_id_auto = tk.Entry(self, state=tk.DISABLED)
        self.entry_id_auto.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self, text="Descripción:").grid(row=3, column=0, padx=10, pady=10)
        self.entry_descripcion = tk.Entry(self, state=tk.DISABLED)
        self.entry_descripcion.grid(row=3, column=1, padx=10, pady=10)

        # Campos de fecha con DateEntry de tkcalendar
        tk.Label(self, text="Fecha de Inicio:").grid(row=4, column=0, padx=10, pady=10)
        self.date_inicio = DateEntry(self, state=tk.DISABLED, date_pattern='yyyy-mm-dd')
        self.date_inicio.grid(row=4, column=1, padx=10, pady=10)

        tk.Label(self, text="Fecha de Entrega:").grid(row=5, column=0, padx=10, pady=10)
        self.date_entrega = DateEntry(self, state=tk.DISABLED, date_pattern='yyyy-mm-dd')
        self.date_entrega.grid(row=5, column=1, padx=10, pady=10)

        # Botones de acción
        self.btn_nuevo = tk.Button(self, text="Nuevo", command=self.nuevo_reparacion)
        self.btn_nuevo.grid(row=6, column=0, padx=10, pady=10)

        self.btn_guardar = tk.Button(self, text="Guardar", state=tk.DISABLED, command=lambda: self.guardar_reparacion(id=self.entry_id_reparacion.get(),
                                                                                                                      id_auto=self.entry_id_auto.get(),
                                                                                                                      descripcion=self.entry_descripcion.get(),
                                                                                                                      fecha_inicio=self.date_inicio.get(),
                                                                                                                      fecha_entrega=self.date_entrega.get()))
        self.btn_guardar.grid(row=6, column=1, padx=10, pady=10)

        self.btn_cancelar = tk.Button(self, text="Cancelar", command=self.cancelar)
        self.btn_cancelar.grid(row=6, column=2, padx=10, pady=10)

        self.btn_editar = tk.Button(self, state=tk.DISABLED, text="Editar", command=self.editar_reparacion)
        self.btn_editar.grid(row=6, column=3, padx=10, pady=10)

        self.btn_eliminar = tk.Button(self, state=tk.DISABLED, text="Eliminar", command=self.eliminar_reparacion)
        self.btn_eliminar.grid(row=6, column=4, padx=10, pady=10)

        # Sección de piezas asociadas a la reparación
        tk.Label(self, text="Piezas asociadas a la reparación:").grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        self.lbl_total = tk.Label(self, text="Total: $0")
        self.lbl_total.grid(row=7, column=2, columnspan=2, padx=10, pady=10)


        # Treeview para mostrar piezas
        self.tree_piezas = ttk.Treeview(self, columns=("ID", "Descripción", "Cantidad"), show="headings", height=5)
        self.tree_piezas.grid(row=8, column=0, columnspan=4, padx=10, pady=10)
        self.tree_piezas.heading("ID", text="ID de Pieza")
        self.tree_piezas.heading("Descripción", text="Descripción de Pieza")
        self.tree_piezas.heading("Cantidad", text="Cantidad")

        # Botones para agregar y quitar piezas
        tk.Button(self, text="Agregar Pieza", command=self.agregar_pieza).grid(row=9, column=0, padx=10, pady=10)
        tk.Button(self, text="Quitar Pieza", command=self.quitar_pieza).grid(row=9, column=1, padx=10, pady=10)


    def cancelar(self):
        self.destroy()
        self.mainwindow.deiconify()

    def limpiar_campos(self, *campos):
        for campo in campos:
            campo.delete(0, tk.END)

    def habilitar_deshabilitar_campos(self, *campos, state):
        for campo in campos:
            campo.config(state=state)

    def buscar_reparacion(self):
        try:
            id_reparacion = self.entry_buscar_id.get()
            if not id_reparacion:
                messagebox.showinfo("Información", "Ingrese un ID de reparación para buscar")
                return
            reparacion = self.db_repo.buscar_reparacion(id_reparacion)
            if reparacion:
                self.habilitar_deshabilitar_campos(self.entry_id_reparacion, self.entry_id_auto,
                                                    self.entry_descripcion, self.date_entrega, self.date_inicio, self.btn_editar, state=tk.NORMAL)
                self.entry_id_reparacion.insert(0, reparacion.id)
                self.entry_id_auto.insert(0, reparacion.id_vehiculo)
                self.entry_descripcion.insert(0, reparacion.descripcion)
                self.date_inicio.set_date(reparacion.fecha_inicio)
                self.date_entrega.set_date(reparacion.fecha_entrega)
                self.tree_piezas.delete(*self.tree_piezas.get_children())

                piezas = self.db_repo.obtener_partes_reparacion(id_reparacion)
                total = 0
                for pieza in piezas:
                    self.tree_piezas.insert("", "end", values=(pieza.id, pieza.nombre, self.db_repo.obtener_cantidad_parte(id_reparacion, pieza.id)))
                    total += pieza.costo * self.db_repo.obtener_cantidad_parte(id_reparacion, pieza.id)

                self.lbl_total.config(text="Total: ${}".format(total))

                self.habilitar_deshabilitar_campos(self.entry_id_reparacion, self.entry_id_auto,
                                                    self.entry_descripcion, self.date_entrega, self.date_inicio, state=tk.DISABLED)
                self.habilitar_deshabilitar_campos(self.btn_eliminar, state=tk.NORMAL)
            else:
                messagebox.showinfo("Información", "Reparación no encontrada")

        except Exception as e:
            messagebox.showerror("Error", "Error al buscar reparación. ({})".format(e))

    def eliminar_reparacion(self):
        try:
            self.db_repo.borrar_reparacion(self.entry_id_reparacion.get())
            messagebox.showinfo("Reparación eliminada", "Reparación eliminada correctamente")
            self.limpiar_campos(self.entry_id_reparacion, self.entry_id_auto, self.entry_descripcion, self.date_inicio, self.date_entrega)
            self.habilitar_deshabilitar_campos(self.entry_id_reparacion, self.entry_id_auto, self.entry_descripcion, self.date_inicio, self.date_entrega, self.btn_editar, self.btn_eliminar, state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", "Error al eliminar reparación. ({})".format(e))

    def editar_reparacion(self):
        self.habilitar_deshabilitar_campos(self.entry_id_auto, self.entry_descripcion, self.date_inicio, self.date_entrega, self.btn_guardar, self.btn_eliminar, state=tk.NORMAL)
        self.habilitar_deshabilitar_campos(self.btn_nuevo, self.entry_id_reparacion, state=tk.DISABLED)

    def nuevo_reparacion(self):
        self.habilitar_deshabilitar_campos(self.entry_id_reparacion, self.entry_id_auto, self.entry_descripcion, self.date_entrega, self.date_inicio, self.btn_guardar, state=tk.NORMAL)
        self.entry_id_reparacion.delete(0, tk.END)
        self.entry_id_reparacion.insert(0, self.db_repo.obtener_siguiente_id_reparaciones())
        self.habilitar_deshabilitar_campos(self.btn_nuevo, self.entry_id_reparacion, self.btn_eliminar, state=tk.DISABLED)

    def guardar_reparacion(self, id, id_auto, descripcion, fecha_inicio, fecha_entrega):
        try:
            id_auto = id_auto.upper()
            self.db_repo.guardar_reparacion(id_reparacion=id, id_vehiculo=id_auto, descripcion=descripcion,
                                            fecha_inicio=fecha_inicio, fecha_entrega=fecha_entrega, id_mecanico=self.user.id)
            
            messagebox.showinfo("Reparación guardada", "Reparación guardada correctamente")
            self.habilitar_deshabilitar_campos(self.btn_nuevo, self.entry_id_reparacion, state=tk.NORMAL)
            self.limpiar_campos(self.entry_id_reparacion, self.entry_id_auto, self.entry_descripcion)
            self.habilitar_deshabilitar_campos(self.entry_id_reparacion, self.entry_id_auto, self.entry_descripcion, self.date_inicio, self.date_entrega, self.btn_guardar, state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", "Error al guardar reparación. ({})".format(e))

    def agregar_pieza(self):
        try:
            # Pedir el ID de la pieza
            pieza_id = simpledialog.askstring("Agregar Pieza", "Ingrese el ID de la pieza:")
            
            # Obtener la descripción de la pieza
            pieza_descripcion = self.db_repo.obtener_nombre_pieza(pieza_id)
            
            if pieza_descripcion:
                # Pedir la cantidad de la pieza
                cantidad = simpledialog.askinteger("Cantidad de Piezas", "Ingrese la cantidad:")
                
                if cantidad and cantidad > 0:
                    # Agregar la pieza a la base de datos y a la lista
                    self.db_repo.agregar_det_rep_parte(id_reparacion=self.entry_id_reparacion.get(), id_parte=pieza_id, cantidad=cantidad)
                    self.tree_piezas.insert("", "end", values=(pieza_id, pieza_descripcion, cantidad))
                    self.calcular_total()
                else:
                    messagebox.showinfo("Información", "La cantidad debe ser un número positivo")
            else:
                messagebox.showinfo("Información", "Pieza no encontrada")
        except Exception as e:
            messagebox.showerror("Error", "Error al agregar pieza. ({})".format(e))

    def quitar_pieza(self):
        # Eliminar la pieza seleccionada
        try:
            selected_item = self.tree_piezas.selection()
            if selected_item:
                pieza_id = self.tree_piezas.item(selected_item)["values"][0]
                self.db_repo.eliminar_det_rep_parte(self.entry_id_reparacion.get(), pieza_id)
                self.tree_piezas.delete(selected_item)

                self.calcular_total()

            else:
                messagebox.showinfo("Información", "Seleccione una pieza para quitar")
        except Exception as e:
            messagebox.showerror("Error", "Error al quitar pieza. ({})".format(e))

    def guardar_piezas(self, id_reparacion):
        try:
            piezas = [self.tree_piezas.item(item)["values"][0] for item in self.tree_piezas.get_children()]
            self.db_repo.guardar_piezas_reparacion(id_reparacion, piezas)
        except Exception as e:
            messagebox.showerror("Error", "Error al guardar piezas. ({})".format(e))

    def calcular_total(self):
        # Calcular el total
        total = 0
        for item in self.tree_piezas.get_children():
            pieza = self.tree_piezas.item(item)
            total += self.db_repo.obtener_costo_pieza(pieza["values"][0]) * pieza["values"][2]

        self.lbl_total.config(text="Total: ${}".format(total))
        
