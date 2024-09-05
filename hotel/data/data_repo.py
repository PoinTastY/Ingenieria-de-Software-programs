import json
import os

from exceptions.habitacionNoEncontrada import HabitacionNoEncontrada
from entities.habitacion import *

def cargar_datos():
    try:
        if os.path.getsize('data/db.json') > 0:  # Verifica que el archivo no esté vacío
            with open('data/db.json', 'r') as archivo:
                print("File found")
                datos = json.load(archivo)
                print("File loaded")
                return datos
        else:
            print("File is empty")
            return {"clientes": [], "reservaciones": [], "habitaciones": []}
    except FileNotFoundError:
        # Si el archivo no existe, retornamos una estructura vacía
        print("File not found")
        return {"clientes": [], "reservaciones": [], "habitaciones": []}
    
def guardar_datos(datos):
    with open('data/db.json', 'w') as archivo:
        json.dump(datos, archivo, indent=4)
    print("datos guardados")
        
def agregar_cliente(datos, id_cliente, nombre, direccion, telefono, email):
    nuevo_cliente = {
        "id": id_cliente,
        "nombre": nombre,
        "direccion": direccion,
        "telefono": telefono,
        "email": email
    }
    datos['clientes'].append(nuevo_cliente)
    guardar_datos(datos)
    print(f"Cliente {nombre} agregado correctamente.")

#reservacion
def agregar_reservacion(datos, id_reserva, cliente_id, habitacion_id, fecha_reserva, fecha_salida, hora_reserva, costo):
    nueva_reservacion = {
        "id": id_reserva,
        "id_cliente": cliente_id,
        "id_habitacion": habitacion_id,
        "fecha_reservacion": fecha_reserva,
        "fecha_salida": fecha_salida,
        "hora_reservacion": hora_reserva,
        "costo": costo
    }
    datos['reservaciones'].append(nueva_reservacion)
    guardar_datos(datos)
    print(f"Reservación {id_reserva} agregada correctamente.")

def buscar_reservacion(datos, reservacion_id):
    for reservacion in datos['reservaciones']:
        if reservacion['id'] == reservacion_id:
            return reservacion
    return None

def buscar_reservaciones_cliente(datos, cliente_id):
    reservaciones_cliente = []
    for reservacion in datos['reservaciones']:
        if reservacion['cliente_id'] == cliente_id:
            reservaciones_cliente.append(reservacion)
    return reservaciones_cliente

def editar_habitacion(datos, habitacion : Habitacion):
    for habitacion in datos['habitaciones']:
        if habitacion['id'] == habitacion.id:
            habitacion['estado'] = habitacion.estado
            habitacion['numero_habitacion'] = habitacion.numero_habitacion
            guardar_datos(datos)
            print(f"Habitación {habitacion.id} actualizada a {habitacion.estado}.")
            return
    raise HabitacionNoEncontrada(f"Habitación con ID {habitacion.id} no encontrada.")


def buscar_cliente(datos, cliente_id):
    for cliente in datos['clientes']:
        if cliente['id'] == cliente_id:
            return cliente
    return None

#habitacion shit
def buscar_habitacion(datos, numero_habitacion: str):
    for habitacion in datos['habitaciones']:
        if habitacion['numero_habitacion'] == numero_habitacion:
            return_room_obj = Habitacion(habitacion['id'], habitacion['numero_habitacion'], habitacion['estado'])
            return return_room_obj
    return None

def agregar_habitacino(datos, habitacion : Habitacion):
    try:
        if(buscar_habitacion(datos, habitacion.id) != None):
            raise Exception(f"Habitacion con id: {habitacion.id} duplicado, verifique que no exista")
        
        nueva_habitacion = {
            "id": datos['indices']['habitaciones'] + 1,
            "numero_habitacion": habitacion.numero_habitacion,
            "estado": habitacion.estado
        }
        datos['habitaciones'].append(nueva_habitacion)
        datos['indices']['habitaciones'] += 1
        guardar_datos(datos)
        print(f"Habitacion {habitacion.id} guardada correctamente.")
    except ValueError as e:
        raise Exception(f"Error: {e}")
    
def eliminar_habitacion(datos, habitacion_id):
    for habitacion in datos['habitaciones']:
        if habitacion['id'] == habitacion_id:
            datos['habitaciones'].remove(habitacion)
            guardar_datos(datos)
            print(f"Habitación {habitacion_id} eliminada.")
            return
    print("Habitación no encontrada.")

def eliminiar_cliente(datos, cliente_id):
    for cliente in datos['clientes']:
        if cliente['id'] == cliente_id:
            datos['clientes'].remove(cliente)
            guardar_datos(datos)
            print(f"Cliente {cliente_id} eliminado.")
            return
    print("Cliente no encontrado.")



