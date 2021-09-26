import builtins
from tkinter import * 
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import *
import sqlite3
import os

#Desarrollo de la interfaz Grafica
#https://www.youtube.com/watch?v=HD5xacNn-5o&t=1812s


app = Tk()
app.title("Reporte de Monitoreos")
app.geometry("600x250")
app.config(bg="lightblue")        
app.resizable(0,0)




miId=StringVar()
miNombre=StringVar()
miCargo=StringVar()
miSalario=StringVar()



def conexionBBDD():
    miConexion=sqlite3.connect("base.db")
    miCursor=miConexion.cursor()
    
    try:
        miCursor.execute('''
                        CREATE TABLE IF NOT EXISTS empleado (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            NOMBRE VARCHAR(250) NOT NULL,
                            CARGO VARCHAR(250) NOT NULL,
                            SALARIO INT NOT NULL)
                         ''')
        messagebox.showinfo("CONEXION", "base.db de Datos Creada Exitosamente")
        
    except:
        messagebox.showinfo("CONEXION","Conexion exitosa con la base.db de datos")
        

def eliminarBBDD():
    miConexion=sqlite3.connect("base.db")
    miCursor=miConexion.cursor()
    if messagebox.askyesno(message="Los datos se perderan definitivamente, desea continuar ?", title="WARNING"):
        miCursor.execute("DROP TABLE empleado")
    else:
        pass
    limpiarCampos()
    mostrar()
    
def salirAplicacion():
    valor=messagebox.askquestion("Salir","Esta seguro que desea salir", title="WARNING")
    if valor=="yes":
        app.destoy()
    
def limpiarCampos():
    miId.set("")
    miNombre.set("")
    miCargo.set("")
    miSalario.set("")
    
def mensaje():
    acerca='''
    Aplicacion CRUD
    version 1.0
    tecnologia Python3 Tkinter
    '''
    messagebox.showinfo(title="Informaciom",message=acerca)

########################################  Reporte #########################################


def crear():
    miConexion=sqlite3.connect("base.db")
    miCursor=miConexion.cursor()
    
    try:
        datos=miNombre.get(),miCargo.get(),miSalario.get()
        miCursor.execute("INSERT INTO empleado VALUES (NULL,?,?,?)", (datos) )
        miConexion.commit()
    except:
        messagebox.showwarning("WARNING","Ocurrio un error al crear el registro, verifique conexion con la DB")
        pass
    limpiarCampos()
    mostrar()
    
def mostrar():
    miConexion=sqlite3.connect("base.db")
    miCursor=miConexion.cursor()
    registros=tree.get_children()
    for elemento in registros:
        tree.delete(elemento)
        
    try:
        miCursor.execute("SELECT * FROM empleado")
        for row in miCursor:
            tree.insert("",0,text=row[0], values=(row[1],row[2],row[3]))
    except:
        pass

    
########################################## Tabla ########################################

tree=ttk.Treeview(height=10, columns=('#0','#1','#2'))
tree.place(x=0, y=130)
tree.column('#0', width=100)
tree.heading('#0', text="ID", anchor=CENTER)
tree.heading('#1', text="Nombre del Empleado", anchor=CENTER)
tree.heading('#2', text="Cargo", anchor=CENTER)
tree.column('#3', width=100)
tree.heading('#3', text="Slario", anchor=CENTER)


#################################### Editables ##########################################

def seleccionarUsandoClick(event):
    item=tree.identify('item', event.x, event.y)
    miId.set(tree.item(item,"text"))
    miNombre.set(tree.item(item,"values")[0])
    miCargo.set(tree.item(item,"values")[1])
    miSalario.set(tree.item(item,"values")[2])
    
tree.bind("<Double-1>", seleccionarUsandoClick)

def actualizar():
    miConexion=sqlite3.connect("base.db")
    miCursor=miConexion.cursor()   
    try:
        datos=miNombre.get(),miCargo.get(),miSalario.get()
        miCursor.execute("UPDATE empleado SET NOMBRE=?, CARGO=?, SALARIO=? WHERE ID="+miId.get(), (datos) )
        miConexion.commit()
    except:
        messagebox.showwarning("WARNING","Ocurrio un error al editar el registro.")
        pass
    limpiarCampos()
    mostrar()
    
def borrar():
    miConexion=sqlite3.connect("base.db")
    miCursor=miConexion.cursor()
            
    try:
        if messagebox.askyesno(message="Desea eliminar el registro", title="Advertencia"):
            miCursor.execute("DELETE FROM empleado WHERE ID="+miId.get())
            miConexion.commit()
    except:
        messagebox.showwarning("WARNING","Ocurrio un error al eliminar el registro.")
        pass
    limpiarCampos()
    mostrar()
    
    
    
############################################### Widgeths ################################################################
        
   #### Menu ###  
        
menubar=Menu(app)
menubasedat=Menu(menubar, tearoff=0)
menubasedat.add_command(label="Crear/Conectar base.db de Datos", command=conexionBBDD)
menubasedat.add_command(label="Delete", command=eliminarBBDD)
menubasedat.add_command(label="Salir", command=salirAplicacion)
menubar.add_cascade(label="Inicio", menu=menubasedat)

ayudamenu=Menu(menubar, tearoff=0)
ayudamenu.add_command(label="Reset Campos", command=limpiarCampos)
ayudamenu.add_command(label="Acerca", command=mensaje)
menubar.add_cascade(label="ayuda", menu=ayudamenu)

#### Etiqueta  - Text Box ####

e1=Entry(app, textvariable=miId)

l2=Label(app, text="Nombre")
l2.place(x=50, y=10)
e2=Entry(app, textvariable=miNombre, width=50)
e2.place(x=100, y=10)

l3=Label(app, text="Cargo")
l3.place(x=50, y=40)
e3=Entry(app, textvariable=miCargo)
e3.place(x=100, y=40)

l4=Label(app, text="Salario")
l4.place(x=280, y=40)
e4=Entry(app, textvariable=miSalario, width=10)
e4.place(x=320, y=40)

l5=Label(app,text="USD")
l5.place(x=390 , y=42)

#### Bottones ####

b1=Button(app, text="Crear Registro", command=crear)
b1.place(x=50, y=90)

b2=Button(app, text="Update", command=actualizar)
b2.place(x=180, y=90)

b3=Button(app, text="Show Register", command=mostrar)
b3.place(x=250, y=90)

b4=Button(app, text="Delete", command=borrar)
b4.place(x=450, y=90)

### Raiz ####

app.config(menu=menubar)
#app.iconbitmap('..\img\imi.ico')


app.mainloop() 
