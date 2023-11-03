from tkinter import ttk
from tkinter import *

import time


import random

import sqlite3

base = sqlite3.connect("Base_de_datos.bd")
cursor = base.cursor()



global preguntas
cursor.execute("Select * from Pregunta")
preguntas = cursor.fetchall()

global preguntas_random
cursor.execute("Select * from Pregunta")
preguntas_random = cursor.fetchall()

random.shuffle(preguntas_random)



global puntos
puntos = 0

global tiempo
tiempo = 0

global tree


def jugar(numero,ventana_anterior,respuesta_anterior):
    global puntos
    global tiempo
    global tree

    

    if numero > 15:

        tiempo = (time.time() - tiempo)

        minutos,segundos = divmod(tiempo, 60)
        
        datos_usuario = [nombre_entry.get(),contacto_entry.get(),puntos,f"{int(minutos)} : {int(segundos)}"]
        print(datos_usuario)

        cursor.execute("INSERT INTO Usuario (nombre, instagram, aciertos, tiempo) VALUES (?, ?, ?, ?)", (datos_usuario[0],datos_usuario[1],datos_usuario[2],datos_usuario[3]))

        base.commit()

        actualizar_tree()
        pass

    else:
        respuestas_random = []
        for i in range(0,4):
            respuestas_random.append(preguntas_random[numero][2 + i])
        random.shuffle(respuestas_random)

        ventana_pregunta = Toplevel(root)
        ventana_pregunta.attributes("-fullscreen", True)

        pregunta_titulo = Label(ventana_pregunta,text=preguntas_random[numero][1])
        pregunta_titulo.pack(pady=100)

        respuesta_1 = Button(ventana_pregunta,text=respuestas_random[0],command= lambda : jugar(numero+1,ventana_pregunta,respuesta_1['text'])  ,width=100,height=2)
        respuesta_1.pack(pady=100)
        respuesta_2 = Button(ventana_pregunta,text=respuestas_random[1],command= lambda : jugar(numero+1,ventana_pregunta,respuesta_2['text'])  ,width=100,height=2)
        respuesta_2.pack()
        respuesta_3 = Button(ventana_pregunta,text=respuestas_random[2],command= lambda : jugar(numero+1,ventana_pregunta,respuesta_3['text'])  ,width=100,height=2)
        respuesta_3.pack(pady=100)
        respuesta_4 = Button(ventana_pregunta,text=respuestas_random[3],command= lambda : jugar(numero+1,ventana_pregunta,respuesta_4['text'])  ,width=100,height=2)
        respuesta_4.pack()

    if (ventana_anterior != 0):

        if respuesta_anterior == preguntas_random[numero-1][2]:
            puntos +=100

        ventana_anterior.destroy()
    else:
        puntos = 0
        tiempo = time.time()


def actualizar_tree():
    global tree
    tree.delete(*tree.get_children())  # Borrar datos existentes en el Treeview
    cursor.execute("select nombre, instagram, aciertos, tiempo from usuario order by aciertos DESC")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)


root = Tk()


titulo = Label(root,text="TITULO DE JUEGO") ; titulo.pack(pady=100)

nombre_label = Label(root,text="Ingrese su nombre") ; nombre_label.pack(pady=10)

nombre_entry = Entry(root) ; nombre_entry.pack(pady=0)

contacto_label = Label(root,text="Ingrese su contacto") ; contacto_label.pack(pady=10)

contacto_entry = Entry(root) ; contacto_entry.pack(pady=0)

boton_jugar = Button(root,text="JUGAR",command= lambda : jugar(0,0,0)) ; boton_jugar.pack(pady=50)

tree = ttk.Treeview(root,columns=("Nombre","Contacto","Puntaje","Tiempo"))

tree.pack()



tree.heading("#1", text="Nombre")
tree.heading("#2", text="Contacto")
tree.heading("#3", text="Puntaje")
tree.heading("#4", text="Tiempo")

tree.column("#0", width=0, stretch=NO)

actualizar_tree()

#tree.insert("",END,NONE,values=("Eleazar","numero whatsapp","100 puntos", "20"))

root.resizable(0,0)  ;  root.attributes("-fullscreen", True)
root.mainloop()