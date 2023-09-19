import tkinter as tk
from tkinter import ttk, messagebox
from model.geolocalizador_dao import crear_tabla, borrar_tabla, Registro, guardar, listar
import datetime



import pandas as pd
import folium
import pyicloud

val = True
api = None


def barra_menu(root):
    barra_menu = tk.Menu(root)
    root.config(menu = barra_menu, width = 300, height = 300 )
    
    menu_inicio = tk.Menu(barra_menu, tearoff = 0)
    barra_menu.add_cascade(label = 'Inicio', menu = menu_inicio)
   
    menu_inicio.add_command(label = 'Salir', command = root.destroy)

    menu_registro = tk. Menu( barra_menu, tearoff= 0)
    barra_menu.add_cascade(label= 'Registros', menu= menu_registro)
    menu_registro.add_command(label = 'Eliminar registro en DB', command= lambda: borrar_tabla())
    
    
class Frame(tk.Frame):
    def __init__(self, root = None):
        super().__init__(root, width= 480, height= 320)
        self.root = root
        self.pack()
        
        self.campos_info()
        self.deshabilitar_campos()

        
    def campos_info(self):
        self.label_correo = tk.Label(self, text = 'Correo: ')
        self.label_correo.config(font=('Arial', 12, 'bold'))
        self.label_correo.grid(row = 0, column = 0, padx= 10, pady= 10)
        
        self.label_contra = tk.Label(self, text = 'Contraseña: ')
        self.label_contra.config(font=('Arial', 12, 'bold'))
        self.label_contra.grid(row = 1, column = 0, padx= 10, pady= 10)
        
        self.label_int = tk.Label(self, text = 'Intervalo de mediciones: ')
        self.label_int.config(font=('Arial', 12, 'bold'))
        self.label_int.grid(row = 0, column = 3, padx= 10, pady= 10)
        
        self.label_nombre = tk.Label(self, text = 'Nombre del registro: ')
        self.label_nombre.config(font=('Arial', 12, 'bold'))
        self.label_nombre.grid(row = 1, column = 3, padx= 10, pady= 10)

        #Entradas de cada campo
        self.mi_correo = tk.StringVar()
        self.entry_correo = tk.Entry(self, textvariable= self.mi_correo)
        self.entry_correo.config(width = 25, font = ('Arial', 12) )
        self.entry_correo.grid(row = 0, column = 1, padx= 10, pady= 10, columnspan=2)
        
        self.mi_contr = tk.StringVar()
        self.entry_contr = tk.Entry(self, textvariable= self.mi_contr)
        self.entry_contr.config(width = 25, font = ('Arial', 12) , show= '*')
        self.entry_contr.grid(row = 1, column = 1, padx= 10, pady= 10, columnspan=2)
        
        self.mi_int = tk.StringVar()
        self.entry_int = tk.Entry(self, textvariable= self.mi_int)
        self.entry_int.config(width = 25, font = ('Arial', 12) )
        self.entry_int.grid(row = 0, column = 4, padx= 10, pady= 10, columnspan=2)
        
        self.mi_nombre = tk.StringVar()
        self.entry_nombre = tk.Entry(self, textvariable= self.mi_nombre)
        self.entry_nombre.config(width = 25, font = ('Arial', 12) )
        self.entry_nombre.grid(row = 1, column = 4, padx= 10, pady= 10, columnspan=2)
        
        #Botones
        self.boton_nuevo = tk.Button(self, text = 'Nuevo', command= self.habilitar_campos)
        self.boton_nuevo.config(width = 15, font = ('Arial', 12,'bold'),
                                fg = '#DAD5D6', bg = '#158645', 
                                cursor = 'hand2', activebackground= '#35BD6F')
        self.boton_nuevo.grid(row = 2, column= 0, padx= 10, pady=10)
        
        self.boton_ejecutar = tk.Button(self, text = 'Ejecutar', command= self.ejecutar)
        self.boton_ejecutar.config(width = 15, font = ('Arial', 12,'bold'),
                                fg = '#DAD5D6', bg = '#1658A2', 
                                cursor = 'hand2', activebackground= '#3586DF')
        self.boton_ejecutar.grid(row = 2, column= 4, padx= 10, pady=10)
        
        self.boton_detener = tk.Button(self, text = 'Detener', command= self.apagar)
        self.boton_detener.config(width = 15, font = ('Arial', 12,'bold'),
                                fg = '#DAD5D6', bg = '#BD152E', 
                                cursor = 'hand2', activebackground= '#E15370')
        self.boton_detener.grid(row = 2, column= 5, padx= 10, pady=10)
        
        
        self.boton_cancelar = tk.Button(self, text = 'Cancelar', command= self.deshabilitar_campos)
        self.boton_cancelar.config(width = 15, font = ('Arial', 12,'bold'),
                                fg = '#DAD5D6', bg = '#BD152E', 
                                cursor = 'hand2', activebackground= '#E15370')
        self.boton_cancelar.grid(row = 2, column= 1, padx= 10, pady=10)
        
        self.boton_mostrarmap = tk.Button(self, text = 'Mostrar mapa', command= self.mostrar_ub)
        self.boton_mostrarmap.config(width = 15, font = ('Arial', 12,'bold'),
                                fg = '#DAD5D6', bg = '#1658A2', 
                                cursor = 'hand2', activebackground= '#3586DF')
        self.boton_mostrarmap.grid(row = 4, column= 4, padx= 10, pady=10)
        
    def habilitar_campos(self):
        self.mi_correo.set('')
        self.mi_contr.set('')
        self.mi_int.set('')
        self.mi_nombre.set('')
        
        self.entry_correo.config(state='normal')
        self.entry_contr.config(state= 'normal')
        self.entry_int.config(state= 'normal')
        self.entry_nombre.config(state = 'normal')   

        self.boton_ejecutar.config(state= 'normal')
        self.boton_cancelar.config(state='normal')
    
    def deshabilitar_campos(self):
        self.mi_correo.set('')
        self.mi_contr.set('')
        self.mi_int.set('')
        self.mi_nombre.set('') 
        
        self.entry_correo.config(state='disabled')
        self.entry_contr.config(state= 'disabled')
        self.entry_int.config(state= 'disabled')
        self.entry_nombre.config(state = 'disabled')   
            
        self.boton_ejecutar.config(state= 'disabled')
        self.boton_detener.config(state='disabled')
        self.boton_cancelar.config(state='disabled')
        self.boton_ejecutar.config(state= 'disabled')
        self.boton_detener.config(state= 'disabled')
        self.boton_mostrarmap.config(state= 'disabled')

    
    def ejecutar(self):
        try: 
            global api, val
            
            if val != False and api == None:
                self.boton_nuevo.config(state= 'disabled')
                self.boton_cancelar.config(state='disabled')
                self.boton_mostrarmap.config(state='disabled')
                self.boton_ejecutar.config(state='disabled')
                self.boton_detener.config(state='normal')
                self.entry_correo.config(state='disabled')
                self.entry_contr.config(state= 'disabled')
                self.entry_int.config(state= 'disabled')
                self.entry_nombre.config(state = 'disabled')
                
                crear_tabla(self.mi_nombre.get())
                
                api = pyicloud.PyiCloudService(self.mi_correo.get(), self.mi_contr.get())
                
            
            if val != False:
                device = api.devices[0]
                location = device.location()
                registro = Registro(
                    datetime.datetime.now().strftime('%D'),datetime.datetime.now().strftime('%H:%M:%S'),float(location['latitude']),float(location['longitude']),float(location['altitude'])
                )
                guardar(self.mi_nombre.get(),registro)
                self.tabla_registros()
                self.after(int(float(self.mi_int.get()) * 1000), self.ejecutar)
            else:
                self.apagar()
        
        except:
            titulo = 'Crear registro'
            mensaje = 'Existe un error en los datos ingresados, presione detener y corrija los datos'
            messagebox.showerror(title= titulo, message= mensaje)

    
    def apagar(self):
        global api, val
        self.boton_nuevo.config(state= 'normal')
        self.boton_cancelar.config(state='normal')
        self.boton_mostrarmap.config(state='normal')
        self.boton_ejecutar.config(state='normal')
        self.boton_detener.config(state='disabled')
        
        self.entry_correo.config(state='normal')
        self.entry_contr.config(state= 'normal')
        self.entry_int.config(state= 'normal')
        self.entry_nombre.config(state = 'normal')
        
        
        api = None
        val = not val
        
    def tabla_registros(self):
        #Recuperar la lista de registros
        self.lista_registros = listar(self.mi_nombre.get())
        
        self.tabla = ttk.Treeview(self, columns = ('Fecha', 'Hora', 'Latitud', 'Longitud', 'Altitud'), height= 20)
        
        self.tabla.grid(row = 3, column= 0, columnspan= 6, sticky = 'nse',padx= 70, pady= 10)
        
        #Scrollbar para la tabla a partir de 10 registros o mas
        self.scroll = ttk.Scrollbar(self, orient= 'vertical', command= self.tabla.yview)
        self.scroll.grid(row = 3, column= 5, sticky= 'nse')
        
        self.tabla.heading('#0', text= 'ID')
        self.tabla.heading('#1', text= 'FECHA')
        self.tabla.heading('#2', text= 'HORA')
        self.tabla.heading('#3', text= 'LATITUD')
        self.tabla.heading('#4', text= 'LONGITUD')
        self.tabla.heading('#5', text= 'ALTITUD')
        
    
        #Iterar la lista de registros
        for r in self.lista_registros:
            self.tabla.insert('',0,text=r[0], values=(r[1],r[2],r[3],r[4],r[5]))
    
    
    def mostrar_ub(self):
        df = pd.read_sql(self.mi_nombre.get(),'sqlite:///database/registros.db')
        ubicaciones = list(zip(df['latitud'],df['longitud']))
        m = folium.Map(location=[19.27584014606073, -99.4683064528518], zoom_start=100)

        folium.PolyLine(ubicaciones).add_to(m)
        m.save(f'img/{self.mi_nombre.get()}.html')
        titulo = 'Guardar mapa'
        mensaje = '''El mapa con la trayectoria ha sido guardado en la carpeta 'img' '''
        messagebox.showinfo(title= titulo, message= mensaje)