from .conexion_db import ConexionDb
from tkinter import messagebox

def crear_tabla(nombre):
    conexion = ConexionDb()
    sql = f'''
    CREATE TABLE {nombre}(
        id_registro INTEGER,
        fecha  VARCHAR(100),
        hora VARCHAR(100),
        latitud REAL(100),
        longitud REAL(100),
        altitud REAL(100),
        PRIMARY KEY(id_registro AUTOINCREMENT)
    )
    '''
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
        titulo = 'Crear registro'
        mensaje = 'Se creo la tabla en la base de datos'
        messagebox.showinfo(title= titulo, message= mensaje)
    except:
        titulo = 'Crear registro'
        mensaje = 'La tabla ya está creada'
        messagebox.showinfo(title= titulo, message= mensaje)

def borrar_tabla(nombre):
    conexion = ConexionDb()
    
    sql = f'DROP TABLE {nombre} '
    
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
        titulo = 'Borrar registro'
        mensaje = f'La tabla {nombre} de la base de datos se borro con exito'
        messagebox.showinfo(title= titulo, message= mensaje)
    except:
        titulo = 'Borrar registro'
        mensaje = 'No hay tabla para borrar'
        messagebox.showerror(title= titulo, message= mensaje)
        
class Registro:
    def __init__(self, fecha, hora,latiud, longitud, altitud):
        self.id_pelicula = None
        self.fecha = fecha
        self.hora = hora
        self.latitud = latiud
        self.longitud = longitud
        self.altitud = altitud
        
    def __str__(self):
        return f'Registro[{self.fecha}, {self.latitud}, {self.longitud}, {self.altitud}]'

def guardar(nombre,registro):
    conexion = ConexionDb()
    
    sql = f"""INSERT INTO {nombre} (fecha, hora, latitud, longitud, altitud)
    VALUES('{registro.fecha}','{registro.hora}','{registro.latitud}','{registro.longitud}', '{registro.altitud}')"""
    
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
    
    except:
        titulo = 'Conexion al registro'
        mensaje = f'''La tabla {nombre} no está creado en la base de datos'''
        messagebox.showerror(titulo, mensaje)
        
def listar(nombre):
    conexion = ConexionDb()
    
    lista_peliculas = []
    sql = f'''SELECT * FROM {nombre} '''
    
    try:
        conexion.cursor.execute(sql)
        lista_peliculas = conexion.cursor.fetchall()
        conexion.cerrar()
    except:
        titulo = 'Conexion al registro'
        mensaje = 'Crea un registro en la base de datos'
        messagebox.showerror(titulo, mensaje)
    return lista_peliculas