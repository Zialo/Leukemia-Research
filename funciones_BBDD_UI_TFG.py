import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import numpy as np
import os.path as path
import os
from os import remove
import warnings
import traceback
warnings.filterwarnings("error")

# Consultas asociadas a la Base de Datos

def conexion(tabla):
    conn = sqlite3.connect(tabla)
    c = conn.cursor()
    return conn, c

def crear_tabla(c, consulta):
    c.execute(consulta)
    
def insertar_datos(c, conn, consulta):
    c.execute(consulta)
    conn.commit()
    
def consulta(conn, consulta):
    resultados = 0
    columnas = []
    cur = conn.cursor()
    cur.execute(consulta)

    rows = cur.fetchall()
    names = cur.description

    for name in names:
        columnas.append(name[0])
        
    #print(columnas)
        
    for row in rows:
        print(row)
        resultados += 1
        
    #print('Resultados encontrados:', resultados)
        
    return rows, names
        
def cerrar_conexion(c, conn):
    c.close()
    conn.close()

# Funciones asociadas a la Interfaz Grafica

def tk_consulta():

    window = Tk()
    window.title('Base de Datos - Consulta')
    window.iconbitmap('Base de Datos/db_icon.ico')
    window.geometry("550x150")
    
    def submit_consulta(*args):
        # Conexion a la Base de Datos
        conn, c = conexion('TFG_DB.db')
        consulta_sql = text_label_consulta.get()
        print(consulta_sql)
        rows1, names1 = consulta(conn, consulta_sql)
        print(rows1, names1)

        # Ejecuto la consulta
        rows, names = consulta(conn, consulta_sql)

        lista_str = ""
        for i in range(len(names)):
            lista_str += "COLUMNA NUM " + str(i + 1) + " - " + names[i][0] + "\n"
        
        if rows == None:
            messagebox.showinfo(message="La consulta introducida no es valida. Por favor, revise que este todo correctamente escrito", title="Aviso de Error")

        r = str(rows)
        x = r.split('),')
        for j in range(len(rows)):
            if j == 0:
                x[j] = x[0].split('[')[1] + ')'
            elif j == (len(rows) -1):
                x[j] = x[-1].split(']')[0]
            else:
                x[j] += ')'
            x[j] = "FILA NUM " + str(j + 1) + ": " + x[j] 


        nombre_fichero = text_label_name.get() + '.txt'
        
        if(nombre_fichero == '.txt'):
            messagebox.showinfo(message="Introduzca un nombre de fichero valido por favor", title="Aviso de Error")
        elif(os.path.isfile('ConsultasBBDD/' + nombre_fichero)):
            messagebox.showinfo(message="El nombre introducido ya existe, por favor, cambielo", title="Aviso de Error")
        else:        
            with open('ConsultasBBDD/' + nombre_fichero, 'w+') as f:
                f.write("################################\n\n")
                f.write("Nombre del fichero: '" + nombre_fichero + "'\n")
                f.write("\n################################\n\n")
                f.write("Consulta en SQL: '" + consulta_sql.upper() + "'\n")
                f.write("\n################################\n\n")
                f.write("Parametros que se muestran en orden de salida:\n\n")
                f.write(lista_str)
                f.write("\n################################\n\n")
                f.write('El resultado de su consulta es:\n\n')
                for item in x:
                    f.write("%s\n" % item)
            messagebox.showinfo(message="Archivo '" + nombre_fichero + "' creado con exito", title="Fichero creado")
    
    
    # Creacion de Text Boxes
    text_label_consulta = Entry(window,  width=30)
    text_label_consulta.grid(row=2, column=1, padx=50, pady=2)
    text_label_name = Entry(window,  width=30)
    text_label_name.grid(row=3, column=1, padx=15, pady=2)

    # Creacion de Text Boxes Labels
    label_1_label = Label(window, text="La consulta sera generada en un fichero .txt")
    label_1_label.grid(row=1, column=0, padx=20, pady=2)
    label_2_label = Label(window, text="Escribe que consulta quieres ejecutar:")
    label_2_label.grid(row=2, column=0, padx=20, pady=2)
    label_3_label = Label(window, text="Guardar consulta en fichero con nombre:")
    label_3_label.grid(row=3, column=0, padx=20, pady=2)

    # Metodos de ejecucion
    button = Button(window, text="Enviar", command=submit_consulta)
    button.grid(row = 4, column=1, columnspan=2, padx=20, pady=10, ipadx=30)

    window.mainloop()

# GUI para introducir datos en la tabla Usuarios
def tk_usuarios(): 

    window = Tk()
    window.title('Base de Datos - Usuarios')
    window.iconbitmap('Base de Datos/db_icon.ico')
    window.geometry("550x700")


    # Creacion de la funcion Submit
    def submit_usuario():
        existe = 0
        
        # Conexion a la Base de Datos
        conn, c = conexion('TFG_DB.db')
        
        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM USUARIOS")
        resultados = c.fetchall()

        for i in range(len(resultados)):
            if (str(usuario_nombre.get()) == str(resultados[i][1]) and str(usuario_apellido1.get()) == str(resultados[i][2]) and str(usuario_apellido2.get()) == str(resultados[i][3])):
                existe = 1
        if existe == 0:
            # Insertamos en la Base de Datos
            insertar_datos(c, conn, "INSERT INTO USUARIOS (nombre, apellido1, apellido2, ultimo_acceso) VALUES('" + usuario_nombre.get() + "','" + usuario_apellido1.get() + "','" + usuario_apellido2.get() + "',  DATETIME('now','localtime'))")
            
            # Limpiamos los Text Boxes
            usuario_nombre.delete(0, END)
            usuario_apellido1.delete(0, END)
            usuario_apellido2.delete(0, END)
        
        else:
             messagebox.showinfo(message="El Usuario introducido ya figura como usuario registrado. Por favor, reviselo de nuevo.", title="Aviso de Error")
        

    # Creacion de la funcion Query
    def query_usuario():
        # Conexion a la Base de Datos
        conn, c = conexion('TFG_DB.db')

        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM USUARIOS")
        resultados = c.fetchall()

        print_resultados = ''
        for resultado in resultados:
            print_resultados += str(resultado[0]) + ' ' + str(resultado[1]) + ' ' + str(resultado[2]) + ' ' + str(resultado[3]) + "\n"

        query_label = Label(frame, text=print_resultados)
        query_label.grid(row=6, column=0, columnspan=2)

        # Guardamos los cambios
        conn.commit()

        # Cerramos la conexion a la Base de Datos
        conn.close()
    
    # Creacion del Scrollbar
    scrollbar = tk.Scrollbar(window)
    
    # Creacion del Canvas
    canvas = Canvas(window, yscrollcommand=scrollbar.set)
    
    scrollbar.config(command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    frame = Frame(canvas)
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window(0,0, window=frame, anchor='nw')
    window.update()
    canvas.config(scrollregion=canvas.bbox("all"))
    
    # Creacion de Text Boxes
    usuario_nombre = Entry(frame, width=30)
    usuario_nombre.grid(row=1, column=1, padx=20, pady=2)
    usuario_apellido1 = Entry(frame, width=30)
    usuario_apellido1.grid(row=2, column=1, padx=20, pady=2)
    usuario_apellido2 = Entry(frame, width=30)
    usuario_apellido2.grid(row=3, column=1, padx=20, pady=2)

    # Creacion de Text Boxes Labels
    usuario_titulo = Label(frame, text="Introduzca los datos del Usuario", font=("Calibri",12),justify="center")
    usuario_titulo.grid(row=0, column=0, padx=20, pady=2)
    usuario_nombre_label = Label(frame, text="Nombre")
    usuario_nombre_label.grid(row=1, column=0, padx=20, pady=2)
    usuario_apellido1_label = Label(frame, text="Primer Apellido")
    usuario_apellido1_label.grid(row=2, column=0, padx=20, pady=2)
    usuario_apellido2_label = Label(frame, text="Segundo Apellido")
    usuario_apellido2_label.grid(row=3, column=0, padx=20, pady=2)

    # Creacion de Submit Button
    usuario_submit_button = Button(frame, text="Introducir Usuario a la Base de Datos", command=submit_usuario)
    usuario_submit_button.grid(row = 4, column=0, columnspan=2, padx=20, pady=10, ipadx=100)

    # Creamos un Query Butoon
    usuario_query_button = Button(frame, text="Mostrar Usuarios en la Base de Datos", command=query_usuario)
    usuario_query_button.grid(row = 5, column=0, columnspan=2, padx=20, pady=10, ipadx=100)

    window.mainloop()

# GUI para introducir datos en la tabla Pruebas
def tk_pruebas():     

    window = Tk()
    window.title('Base de Datos - Pruebas')
    window.iconbitmap('Base de Datos/db_icon.ico')
    window.geometry("550x700")


    # Creacion de la funcion Submit
    def submit_prueba():
        existe = 0

        # Conexion a la Base de Datos
        conn, c = conexion('TFG_DB.db')

        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM USUARIOS")
        resultados = c.fetchall()

        for i in range(len(resultados)):
            if int(prueba_id_user.get()) == int(resultados[i][0]):
                existe = 1
        if existe == 1:
            # Insertamos en la Base de Datos
            insertar_datos(c, conn, "INSERT INTO PRUEBAS (id_user, fecha, version) VALUES('" + prueba_id_user.get() + "','" + prueba_fecha.get() + "','" + prueba_version.get() + "')")

            # Limpiamos los Text Boxes
            prueba_id_user.delete(0, END)
            prueba_fecha.delete(0, END)
            prueba_version.delete(0, END)

        elif existe == 0:
            messagebox.showinfo(message="El Id_User introducido no figura con el de ningun usuario registrado. Por favor, reviselo y vuelva a introducirlo.", title="Aviso de Error")

    # Creacion de la funcion Query
    def query_prueba():
        # Conexion a la Base de Datos
        conn, c = conexion('TFG_DB.db')

        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM PRUEBAS")
        resultados = c.fetchall()

        print_resultados = ''
        for resultado in resultados:
            print_resultados += str(resultado[0]) + ' ' + str(resultado[1]) + ' ' + str(resultado[2]) + ' ' + str(resultado[3]) + "\n"

        query_label = Label(window, text=print_resultados)
        query_label.grid(row=6, column=0, columnspan=2)

        # Guardamos los cambios
        conn.commit()

        # Cerramos la conexion a la Base de Datos
        conn.close()

    # Creacion de Text Boxes
    prueba_id_user = Entry(window, width=30)
    prueba_id_user.grid(row=1, column=1, padx=20, pady=2)
    prueba_fecha = Entry(window, width=30)
    prueba_fecha.grid(row=2, column=1, padx=20, pady=2)
    prueba_version = Entry(window, width=30)
    prueba_version.grid(row=3, column=1, padx=20, pady=2)

    # Creacion de Text Boxes Labels
    prueba_titulo = Label(window, text="Introduzca los datos de la Prueba", font=("Calibri",12),justify="center")
    prueba_titulo.grid(row=0, column=0, padx=20, pady=2)
    prueba_id_user_label = Label(window, text="Id Usuario")
    prueba_id_user_label.grid(row=1, column=0, padx=20, pady=2)
    prueba_fecha_label = Label(window, text="Fecha (AAAA-MM-DD)")
    prueba_fecha_label.grid(row=2, column=0, padx=20, pady=2)
    prueba_version_label = Label(window, text="Version")
    prueba_version_label.grid(row=3, column=0, padx=20, pady=2)

    # Creacion de Submit Button
    prueba_submit_button = Button(window, text="Introducir Prueba a la Base de Datos", command=submit_prueba)
    prueba_submit_button.grid(row = 4, column=0, columnspan=2, padx=20, pady=10, ipadx=100)

    # Creamos un Query Butoon
    prueba_query_button = Button(window, text="Mostrar Pruebas en la Base de Datos", command=query_prueba)
    prueba_query_button.grid(row = 5, column=0, columnspan=2, padx=20, pady=10, ipadx=100)

    window.mainloop()

# GUI para introducir datos en la tabla Caracteristicas
def tk_caracteristicas():     

    window = Tk()
    window.title('Base de Datos - Caracteristicas')
    window.iconbitmap('Base de Datos/db_icon.ico')
    window.geometry("550x700")


    # Creacion de la funcion Submit
    def submit_caracteristica():
        existe = 0

        # Conexion a la Base de Datos
        conn, c = conexion('TFG_DB.db')

        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM CARACTERISTICAS")
        resultados = c.fetchall()

        for i in range(len(resultados)):
            if str(caracteristicas_nombre.get()) == str(resultados[i][1]):
                existe = 1
        if existe == 0:
            # Insertamos en la Base de Datos
            insertar_datos(c, conn, "INSERT INTO CARACTERISTICAS (nombre) VALUES('" + caracteristicas_nombre.get() + "')")

            # Limpiamos los Text Boxes
            caracteristicas_nombre.delete(0, END)

        elif existe == 1:
            messagebox.showinfo(message="La caracteristica introducida ya figura en la Base de Datos. Por favor, revisela y vuelva a introducirla.", title="Aviso de Error")

    # Creacion de la funcion Query
    def query_caracteristica():
        # Conexion a la Base de Datos
        conn, c = conexion('TFG_DB.db')

        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM CARACTERISTICAS")
        resultados = c.fetchall()

        print_resultados = ''
        for resultado in resultados:
            print_resultados += str(resultado[0]) + ' ' + str(resultado[1]) + "\n"

        query_label = Label(window, text=print_resultados)
        query_label.grid(row=4, column=0, columnspan=2)

        # Guardamos los cambios
        conn.commit()

        # Cerramos la conexion a la Base de Datos
        conn.close()

    # Creacion de Text Boxes
    caracteristicas_nombre = Entry(window, width=30)
    caracteristicas_nombre.grid(row=1, column=1, padx=20, pady=2)

    # Creacion de Text Boxes Labels
    caracteristicas_titulo = Label(window, text="Introduzca los datos de la Caracteristica", font=("Calibri",12),justify="center")
    caracteristicas_titulo.grid(row=0, column=0, padx=20, pady=2)
    caracteristicas_nombre_label = Label(window, text="Nombre")
    caracteristicas_nombre_label.grid(row=1, column=0, padx=20, pady=2)

    # Creacion de Submit Button
    caracteristicas_submit_button = Button(window, text="Introducir Caracteristica a la Base de Datos", command=submit_caracteristica)
    caracteristicas_submit_button.grid(row = 2, column=0, columnspan=2, padx=20, pady=10, ipadx=100)

    # Creamos un Query Butoon
    caracteristicas_query_button = Button(window, text="Mostrar Caracteristicas en la Base de Datos", command=query_caracteristica)
    caracteristicas_query_button.grid(row = 3, column=0, columnspan=2, padx=20, pady=10, ipadx=100)

    window.mainloop()

# GUI para introducir datos en la tabla Clasificadores
def tk_clasificadores():  

    window = Tk()
    window.title('Base de Datos - Clasificadores')
    window.iconbitmap('Base de Datos/db_icon.ico')
    window.geometry("550x700")


    # Creacion de la funcion Submit
    def submit_clasificador():
        existe = 0

        # Conexion a la Base de Datos
        conn, c = conexion('TFG_DB.db')

        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM CLASIFICADORES")
        resultados = c.fetchall()

        clasificadores_normalizacion = ["No", "MinMax", "Standard"]

        for i in range(len(resultados)):
            if str(clasificadores_nombre.get()) == str(resultados[i][1]):
                existe = 1
        if existe == 0:
            # Insertamos en la Base de Datos
            for i in range(len(clasificadores_normalizacion)):
                insertar_datos(c, conn, "INSERT INTO CLASIFICADORES (nombre, normalizacion) VALUES('" + clasificadores_nombre.get() + "', '" + clasificadores_normalizacion[i] + "')")

            # Limpiamos los Text Boxes
            clasificadores_nombre.delete(0, END)

        elif existe == 1:
            messagebox.showinfo(message="El clasificador introducido ya figura en la Base de Datos. Por favor, reviselo y vuelva a introducirlo.", title="Aviso de Error")

    # Creacion de la funcion Query
    def query_clasificador():
        # Conexion a la Base de Datos
        conn, c = conexion('TFG_DB.db')

        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM CLASIFICADORES")
        resultados = c.fetchall()

        print_resultados = ''
        for resultado in resultados:
            print_resultados += str(resultado[0]) + ' ' + str(resultado[1]) + ' ' + str(resultado[2]) + "\n"

        query_label = Label(window, text=print_resultados)
        query_label.grid(row=4, column=0, columnspan=2)

        # Guardamos los cambios
        conn.commit()

        # Cerramos la conexion a la Base de Datos
        conn.close()

    # Creacion de Text Boxes
    clasificadores_nombre = Entry(window, width=30)
    clasificadores_nombre.grid(row=1, column=1, padx=20, pady=2)

    # Creacion de Text Boxes Labels
    clasificadores_titulo = Label(window, text="Introduzca los datos del Clasificador", font=("Calibri",12),justify="center")
    clasificadores_titulo.grid(row=0, column=0, padx=20, pady=2)
    clasificadores_nombre_label = Label(window, text="Nombre")
    clasificadores_nombre_label.grid(row=1, column=0, padx=20, pady=2)

    # Creacion de Submit Button
    clasificadores_submit_button = Button(window, text="Introducir Clasificador a la Base de Datos", command=submit_clasificador)
    clasificadores_submit_button.grid(row = 2, column=0, columnspan=2, padx=20, pady=10, ipadx=100)

    # Creamos un Query Butoon
    clasificadores_query_button = Button(window, text="Mostrar Clasificadores en la Base de Datos", command=query_clasificador)
    clasificadores_query_button.grid(row = 3, column=0, columnspan=2, padx=20, pady=10, ipadx=100)

    window.mainloop()

# GUI para introducir datos en la tabla Pruebas_Clasificadores
def tk_pruebas_clasificadores(): 
    
    window = Tk()
    window.title('Base de Datos - Pruebas_Clasificadores')
    window.iconbitmap('Base de Datos/db_icon.ico')
    window.geometry("550x700")


    # Creacion de la funcion Submit
    def submit_prueba_clasificador():
        existe_prueba = 0
        existe_clasificador = 0
        existe = 0

        # Conexion a la Base de Datos
        conn, c = conexion('TFG_DB.db')

        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM CLASIFICADORES")
        resultados_1 = c.fetchall()

        c.execute("SELECT *, oid FROM PRUEBAS")
        resultados_2 = c.fetchall()

        c.execute("SELECT *, oid FROM PRUEBAS_CLASIFICADORES")
        resultados_3 = c.fetchall()

        for i in range(len(resultados_1)):
            if str(pruebas_clasificadores_id_clasificador.get()) == str(resultados_1[i][0]):
                existe_clasificador = 1

        for i in range(len(resultados_2)):
            if str(pruebas_clasificadores_id_prueba.get()) == str(resultados_2[i][0]):
                existe_prueba = 1

        for i in range(len(resultados_3)):
            if (str(pruebas_clasificadores_id_prueba.get()) == str(resultados_3[i][0]) and str(pruebas_clasificadores_id_clasificador.get()) == str(resultados_3[i][1])):
                existe = 1

        if (existe_clasificador == 1 and existe_prueba == 1 and existe == 0):
            # Insertamos en la Base de Datos
            for i in range(len(clasificadores_normalizacion)):
                insertar_datos(c, conn, "INSERT INTO PRUEBAS_CLASIFICADORES (id_prueba, id_clasificador, porcentaje_de_acierto) VALUES('" + pruebas_clasificadores_id_prueba.get() + "', '" + pruebas_clasificadores_id_clasificador.get() + "', '" + pruebas_clasificadores_porcentaje.get()  + "')")

            # Limpiamos los Text Boxes
            pruebas_clasificadores_porcentaje.delete(0, END)
            pruebas_clasificadores_id_prueba.delete(0, END)
            pruebas_clasificadores_id_clasificador.delete(0, END)

        elif existe_clasificador == 0:
            messagebox.showinfo(message="El clasificador introducido no figura en la Base de Datos. Por favor, reviselo y vuelva a introducirlo.", title="Aviso de Error")

        elif existe_prueba == 0:
            messagebox.showinfo(message="La prueba introducida no figura en la Base de Datos. Por favor, revisela y vuelva a introducirla.", title="Aviso de Error")

        elif existe == 1:
            messagebox.showinfo(message="El resultado introducido ya figura en la Base de Datos. Por favor, reviselo y vuelva a introducirlo.", title="Aviso de Error")

    # Creacion de la funcion Query
    def query_prueba_clasificador():
        # Conexion a la Base de Datos
        conn, c = conexion('TFG_DB.db')

        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM PRUEBAS_CLASIFICADORES ORDER BY porcentaje_de_acierto DESC")
        resultados = c.fetchall()

        if len(resultados) > 20:
            print_resultados = 'Los 20 mejores resultados: \n\n'
            for i in range(20):
                print_resultados += str(resultados[i][0]) + ' ' + str(resultados[i][1]) + ' ' + str(resultados[i][2]) + "\n"
        elif len(resultados) > 10:
            print_resultados = 'Los 10 mejores resultados: \n\n'
            for i in range(10):
                print_resultados += str(resultados[i][0]) + ' ' + str(resultados[i][1]) + ' ' + str(resultados[i][2]) + "\n"
        else:
            print_resultados = ''
            for resultado in resultados:
                print_resultados += str(resultado[0]) + ' ' + str(resultado[1]) + ' ' + str(resultado[2]) + "\n"

        query_label = Label(window, text=print_resultados)
        query_label.grid(row=6, column=0, columnspan=2)

        # Guardamos los cambios
        conn.commit()

        # Cerramos la conexion a la Base de Datos
        conn.close()

    # Creacion de Text Boxes
    pruebas_clasificadores_id_prueba = Entry(window, width=30)
    pruebas_clasificadores_id_prueba.grid(row=1, column=1, padx=20, pady=2)
    pruebas_clasificadores_id_clasificador = Entry(window, width=30)
    pruebas_clasificadores_id_clasificador.grid(row=2, column=1, padx=20, pady=2)
    pruebas_clasificadores_porcentaje = Entry(window, width=30)
    pruebas_clasificadores_porcentaje.grid(row=3, column=1, padx=20, pady=2)

    # Creacion de Text Boxes Labels
    pruebas_clasificadores_titulo = Label(window, text="Introduzca los resultados obtenidos", font=("Calibri",12),justify="center")
    pruebas_clasificadores_titulo.grid(row=0, column=0, padx=20, pady=2)
    pruebas_clasificadores_id_prueba_label = Label(window, text="Id_Prueba")
    pruebas_clasificadores_id_prueba_label.grid(row=1, column=0, padx=20, pady=2)
    pruebas_clasificadores_id_prueba_label = Label(window, text="Id_Clasificador")
    pruebas_clasificadores_id_prueba_label.grid(row=2, column=0, padx=20, pady=2)
    pruebas_clasificadores_id_prueba_label = Label(window, text="Porcentaje(con dos decimales)")
    pruebas_clasificadores_id_prueba_label.grid(row=3, column=0, padx=20, pady=2)

    # Creacion de Submit Button
    pruebas_clasificadores_submit_button = Button(window, text="Introducir Resultado a la Base de Datos", command=submit_prueba_clasificador)
    pruebas_clasificadores_submit_button.grid(row = 4, column=0, columnspan=2, padx=20, pady=10, ipadx=100)

    # Creamos un Query Butoon
    pruebas_clasificadores_query_button = Button(window, text="Mostrar resultados en la Base de Datos", command=query_prueba_clasificador)
    pruebas_clasificadores_query_button.grid(row = 5, column=0, columnspan=2, padx=20, pady=10, ipadx=100)

    window.mainloop()

# GUI para introducir datos en la tabla Pruebas_Caracteristicas
def tk_pruebas_caracteristicas():    

    window = Tk()
    window.title('Base de Datos - Pruebas_Caracteristicas')
    window.iconbitmap('Base de Datos/db_icon.ico')
    window.geometry("550x700")


    # Creacion de la funcion Submit
    def submit_prueba_caracteristica():
        existe_prueba = 0
        existe_caracteristica = 0
        existe = 0

        # Conexion a la Base de Datos
        conn, c = conexion('TFG_DB.db')

        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM CARACTERISTICAS")
        resultados_1 = c.fetchall()

        c.execute("SELECT *, oid FROM PRUEBAS")
        resultados_2 = c.fetchall()

        c.execute("SELECT *, oid FROM PRUEBAS_CARACTERISTICAS")
        resultados_3 = c.fetchall()

        for i in range(len(resultados_1)):
            if str(pruebas_caracteristicas_id_caracteristica.get()) == str(resultados_1[i][0]):
                existe_caracteristica = 1

        for i in range(len(resultados_2)):
            if str(pruebas_caracteristicas_id_prueba.get()) == str(resultados_2[i][0]):
                existe_prueba = 1

        for i in range(len(resultados_3)):
            if (str(pruebas_caracteristicas_id_prueba.get()) == str(resultados_3[i][0]) and str(pruebas_caracteristicas_id_caracteristica.get()) == str(resultados_3[i][1])):
                existe = 1

        if (existe_caracteristica == 1 and existe_prueba == 1 and existe == 0):
            # Insertamos en la Base de Datos
            insertar_datos(c, conn, "INSERT INTO PRUEBAS_CARACTERISTICAS (id_prueba, id_caracteristica) VALUES('" + pruebas_caracteristicas_id_prueba.get() + "', '" + pruebas_caracteristicas_id_caracteristica.get() + "')")

            # Limpiamos los Text Boxes
            pruebas_caracteristicas_id_prueba.delete(0, END)
            pruebas_caracteristicas_id_caracteristica.delete(0, END)

        elif existe_caracteristica == 0:
            messagebox.showinfo(message="La caracteristica introducida no figura en la Base de Datos. Por favor, revisela y vuelva a introducirla.", title="Aviso de Error")

        elif existe_prueba == 0:
            messagebox.showinfo(message="La prueba introducida no figura en la Base de Datos. Por favor, revisela y vuelva a introducirla.", title="Aviso de Error")

        elif existe == 1:
            messagebox.showinfo(message="El resultado introducido ya figura en la Base de Datos. Por favor, reviselo y vuelva a introducirlo.", title="Aviso de Error")

    # Creacion de la funcion Query
    def query_prueba_caracteristica():
        # Conexion a la Base de Datos
        conn, c = conexion('TFG_DB.db')

        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM PRUEBAS_CARACTERISTICAS")
        resultados = c.fetchall()

        print_resultados = ''
        for resultado in resultados:
            print_resultados += str(resultado[0]) + ' ' + str(resultado[1]) + "\n"

        query_label = Label(window, text=print_resultados)
        query_label.grid(row=5, column=0, columnspan=2)

        # Guardamos los cambios
        conn.commit()

        # Cerramos la conexion a la Base de Datos
        conn.close()

    # Creacion de Text Boxes
    pruebas_caracteristicas_id_prueba = Entry(window, width=30)
    pruebas_caracteristicas_id_prueba.grid(row=1, column=1, padx=20, pady=2)
    pruebas_caracteristicas_id_caracteristica = Entry(window, width=30)
    pruebas_caracteristicas_id_caracteristica.grid(row=2, column=1, padx=20, pady=2)

    # Creacion de Text Boxes Labels
    pruebas_caracteristicas_titulo = Label(window, text="Introduzca los resultados", font=("Calibri",12),justify="center")
    pruebas_caracteristicas_titulo.grid(row=0, column=0, padx=20, pady=2)
    pruebas_caracteristicas_id_prueba_label = Label(window, text="Id_Prueba")
    pruebas_caracteristicas_id_prueba_label.grid(row=1, column=0, padx=20, pady=2)
    pruebas_caracteristicas_id_caracteristica_label = Label(window, text="Id_Caracteristica")
    pruebas_caracteristicas_id_caracteristica_label.grid(row=2, column=0, padx=20, pady=2)

    # Creacion de Submit Button
    pruebas_caracteristicas_submit_button = Button(window, text="Introducir Resultado a la Base de Datos", command=submit_prueba_caracteristica)
    pruebas_caracteristicas_submit_button.grid(row = 3, column=0, columnspan=2, padx=20, pady=10, ipadx=100)

    # Creamos un Query Butoon
    pruebas_caracteristicas_query_button = Button(window, text="Mostrar resultados en la Base de Datos", command=query_prueba_caracteristica)
    pruebas_caracteristicas_query_button.grid(row = 4, column=0, columnspan=2, padx=20, pady=10, ipadx=100)

    window.mainloop()
    
# GUI para introducir datos en la tabla Clasificador_Parametros
def tk_clasificadores_parametros():

    window = Tk()
    window.title('Base de Datos - Clasificador_Parametros')
    window.iconbitmap('Base de Datos/db_icon.ico')
    window.geometry("600x700")


    # Creacion de la funcion Submit
    def submit_clasificador_parametro():
        existe = 0
        existe_conjunto = 0

        # Conexion a la Base de Datos
        conn, c = conexion('TFG_DB.db')

        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM CLASIFICADORES")
        resultados = c.fetchall()

        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM CLASIFICADOR_PARAMETROS")
        resultados_2 = c.fetchall()

        for i in range(len(resultados_2)):
            if (str(clasificador_parametros_id_clasificador.get()) == str(resultados_2[i][0]) and str(clasificador_parametros_nombre_parametro.get()) == str(resultados_2[i][1])):
                existe_conjunto = 1

        for i in range(len(resultados)):
            if str(clasificador_parametros_id_clasificador.get()) == str(resultados[i][0]):
                existe = 1

        if existe_conjunto == 0 and existe == 1:
            # Insertamos en la Base de Datos
            # Como cada parametro es valido para tres clasificadores al tener 3 normalizaciones, metemos el valor en los tres
            primer_id = (int((int(clasificador_parametros_id_clasificador.get())-1) / 3) + 1) * 3 - 2
            for id_clasificador_seguida in range(primer_id, primer_id+3):
                insertar_datos(c, conn, "INSERT INTO CLASIFICADOR_PARAMETROS (id_clasificador, nombre_parametro) VALUES('" + str(id_clasificador_seguida) + "', '" + clasificador_parametros_nombre_parametro.get() + "')")

            # Limpiamos los Text Boxes
            clasificador_parametros_id_clasificador.delete(0, END)
            clasificador_parametros_nombre_parametro.delete(0, END)

        elif existe == 0:
            messagebox.showinfo(message="El clasificador introducido no figura en la Base de Datos. Por favor, reviselo y vuelva a introducirlo.", title="Aviso de Error")

        elif existe_conjunto == 1:
            messagebox.showinfo(message="El parametro introducido ya figura en la Base de Datos dentro de ese clasificador. Le recordamos que cada insercion se realiza en los tres clasificadores con distintas normalizaciones. Por favor, reviselo y vuelva a introducirlo.", title="Aviso de Error")

    # Creacion de la funcion Query
    def query_clasificador_parametro():
        # Conexion a la Base de Datos
        conn, c = conexion('TFG_DB.db')

        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM CLASIFICADOR_PARAMETROS ORDER BY id_clasificador")
        resultados = c.fetchall()

        print_resultados = ''
        for resultado in resultados:
            print_resultados += str(resultado[0]) + ' ' + str(resultado[1]) + "\n"

        query_label = Label(window, text=print_resultados)
        query_label.grid(row=5, column=0, columnspan=2)

        # Guardamos los cambios
        conn.commit()

        # Cerramos la conexion a la Base de Datos
        conn.close()

    # Creacion de Text Boxes
    clasificador_parametros_id_clasificador = Entry(window, width=30)
    clasificador_parametros_id_clasificador.grid(row=1, column=1, padx=20, pady=2)

    clasificador_parametros_nombre_parametro = Entry(window, width=30)
    clasificador_parametros_nombre_parametro.grid(row=2, column=1, padx=20, pady=2)

    # Creacion de Text Boxes Labels
    clasificador_parametros_titulo = Label(window, text="Introduzca los datos del Clasificador", font=("Calibri",12),justify="center")
    clasificador_parametros_titulo.grid(row=0, column=0, padx=20, pady=2)
    clasificador_parametros_id_clasificador_label = Label(window, text="Id_Clasificador")
    clasificador_parametros_id_clasificador_label.grid(row=1, column=0, padx=20, pady=2)
    clasificador_parametros_nombre_parametro_label = Label(window, text="Nombre del Parametro")
    clasificador_parametros_nombre_parametro_label.grid(row=2, column=0, padx=20, pady=2)

    # Creacion de Submit Button
    clasificador_parametros_submit_button = Button(window, text="Introducir Parametros a la Base de Datos", command=submit_clasificador_parametro)
    clasificador_parametros_submit_button.grid(row = 3, column=0, columnspan=2, padx=20, pady=10, ipadx=100)

    # Creamos un Query Butoon
    clasificador_parametros_query_button = Button(window, text="Mostrar Parametros en la Base de Datos", command=query_clasificador_parametro)
    clasificador_parametros_query_button.grid(row = 4, column=0, columnspan=2, padx=20, pady=10, ipadx=100)

    window.mainloop()
    
# GUI para introducir datos en la tabla Pruebas_Clasificador_Parametros    
def tk_pruebas_clasificadores_parametros():

    window = Tk()
    window.title('Base de Datos - Pruebas_Clasificador_Parametros')
    window.iconbitmap('Base de Datos/db_icon.ico')
    window.geometry("600x700")


    # Creacion de la funcion Submit
    def submit_pruebas_clasificador_parametro():
        existe_clasificador = 0
        existe_conjunto = 0
        existe_prueba = 0
        existe_parametro = 0

        # Conexion a la Base de Datos
        conn, c = conexion('TFG_DB.db')

        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM CLASIFICADORES")
        resultados = c.fetchall()

        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM PRUEBAS_CLASIFICADOR_PARAMETROS")
        resultados_2 = c.fetchall()

        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM PRUEBAS")
        resultados_3 = c.fetchall()

        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM CLASIFICADOR_PARAMETROS")
        resultados_4 = c.fetchall()

        for i in range(len(resultados_2)):
            if (str(pruebas_clasificador_parametros_id_prueba.get()) == str(resultados_2[i][0]) and str(pruebas_clasificador_parametros_id_clasificador.get()) == str(resultados_2[i][1]) and str(pruebas_clasificador_parametros_nombre_parametro.get()) == str(resultados_2[i][2])):
                existe_conjunto = 1

        for i in range(len(resultados)):
            if str(pruebas_clasificador_parametros_id_clasificador.get()) == str(resultados[i][0]):
                existe_clasificador = 1

        for i in range(len(resultados_3)):
            if str(pruebas_clasificador_parametros_id_prueba.get()) == str(resultados_3[i][0]):
                existe_prueba = 1

        for i in range(len(resultados_4)):
            if str(pruebas_clasificador_parametros_nombre_parametro.get()) == str(resultados_4[i][1]):
                existe_parametro = 1

        if existe_conjunto == 0 and existe_clasificador == 1 and existe_prueba == 1 and existe_parametro == 1:
            # Insertamos en la Base de Datos
            insertar_datos(c, conn, "INSERT INTO PRUEBAS_CLASIFICADOR_PARAMETROS (id_prueba, id_clasificador, nombre_parametro, valor) VALUES('" + pruebas_clasificador_parametros_id_prueba.get() + "', '" + pruebas_clasificador_parametros_id_clasificador.get() + "', '" + pruebas_clasificador_parametros_nombre_parametro.get() + "', '" + pruebas_clasificador_parametros_valor.get() + "')")

            # Limpiamos los Text Boxes
            pruebas_clasificador_parametros_id_prueba.delete(0, END)
            pruebas_clasificador_parametros_id_clasificador.delete(0, END)
            pruebas_clasificador_parametros_nombre_parametro.delete(0, END)
            pruebas_clasificador_parametros_valor.delete(0, END)

        elif existe_prueba == 0:
            messagebox.showinfo(message="La prueba introducida no figura en la Base de Datos. Por favor, revisela y vuelva a introducirla.", title="Aviso de Error")

        elif existe_clasificador == 0:
            messagebox.showinfo(message="El clasificador introducido no figura en la Base de Datos. Por favor, reviselo y vuelva a introducirlo.", title="Aviso de Error")

        elif existe_parametro == 0:
            messagebox.showinfo(message="El parametro introducido no figura en la Base de Datos. Por favor, reviselo y vuelva a introducirlo.", title="Aviso de Error")

        elif existe_conjunto == 1:
            messagebox.showinfo(message="El conjunto introducido ya figura con valor en la Base de Datos dentro de ese clasificador. Por favor, reviselo y vuelva a introducirlo.", title="Aviso de Error")

    # Creacion de la funcion Query
    def query_pruebas_clasificador_parametro():
        # Conexion a la Base de Datos
        conn, c = conexion('TFG_DB.db')

        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM PRUEBAS_CLASIFICADOR_PARAMETROS ORDER BY id_prueba, id_clasificador")
        resultados = c.fetchall()

        print_resultados = ''
        for resultado in resultados:
            print_resultados += str(resultado[0]) + ' ' + str(resultado[1]) + ' ' + str(resultado[2]) + ' ' + str(resultado[3]) + "\n"

        query_label = Label(window, text=print_resultados)
        query_label.grid(row=7, column=0, columnspan=2)

        # Guardamos los cambios
        conn.commit()

        # Cerramos la conexion a la Base de Datos
        conn.close()

    # Creacion de Text Boxes
    pruebas_clasificador_parametros_id_prueba = Entry(window, width=30)
    pruebas_clasificador_parametros_id_prueba.grid(row=1, column=1, padx=20, pady=2)
    pruebas_clasificador_parametros_id_clasificador = Entry(window, width=30)
    pruebas_clasificador_parametros_id_clasificador.grid(row=2, column=1, padx=20, pady=2)
    pruebas_clasificador_parametros_nombre_parametro = Entry(window, width=30)
    pruebas_clasificador_parametros_nombre_parametro.grid(row=3, column=1, padx=20, pady=2)
    pruebas_clasificador_parametros_valor = Entry(window, width=30)
    pruebas_clasificador_parametros_valor.grid(row=4, column=1, padx=20, pady=2)

    # Creacion de Text Boxes Labels
    pruebas_clasificador_parametros_titulo = Label(window, text="Introduzca los datos del Clasificador", font=("Calibri",12),justify="center")
    pruebas_clasificador_parametros_titulo.grid(row=0, column=0, padx=20, pady=2)
    pruebas_clasificador_parametros_id_prueba_label = Label(window, text="Id_Prueba")
    pruebas_clasificador_parametros_id_prueba_label.grid(row=1, column=0, padx=20, pady=2)
    pruebas_clasificador_parametros_id_clasificador_label = Label(window, text="Id_Clasificador")
    pruebas_clasificador_parametros_id_clasificador_label.grid(row=2, column=0, padx=20, pady=2)
    pruebas_clasificador_parametros_nombre_parametro_label = Label(window, text="Nombre del Parametro")
    pruebas_clasificador_parametros_nombre_parametro_label.grid(row=3, column=0, padx=20, pady=2)
    pruebas_clasificador_parametros_valor_label = Label(window, text="Valor")
    pruebas_clasificador_parametros_valor_label.grid(row=4, column=0, padx=20, pady=2)

    # Creacion de Submit Button
    pruebas_clasificador_parametros_submit_button = Button(window, text="Introducir Valor del Parametro a la Base de Datos", command=submit_pruebas_clasificador_parametro)
    pruebas_clasificador_parametros_submit_button.grid(row = 5, column=0, columnspan=2, padx=20, pady=10, ipadx=100)

    # Creamos un Query Butoon
    clasificador_parametros_query_button = Button(window, text="Mostrar Valor de los Parametros en la Base de Datos", command=query_pruebas_clasificador_parametro)
    clasificador_parametros_query_button.grid(row = 6, column=0, columnspan=2, padx=20, pady=10, ipadx=100)

    window.mainloop()
    
# GUI para introducir datos en la tabla Pruebas_Clasificador_Parametros
def tk_pruebas_clasificadores_parametros():

    window = Tk()
    window.title('Base de Datos - Pruebas_Clasificador_Parametros')
    window.iconbitmap('Base de Datos/db_icon.ico')
    window.geometry("600x700")


    # Creacion de la funcion Submit
    def submit_pruebas_clasificador_parametro():
        existe_clasificador = 0
        existe_conjunto = 0
        existe_prueba = 0
        existe_parametro = 0

        # Conexion a la Base de Datos
        conn, c = conexion('TFG_DB.db')

        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM CLASIFICADORES")
        resultados = c.fetchall()

        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM PRUEBAS_CLASIFICADOR_PARAMETROS")
        resultados_2 = c.fetchall()

        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM PRUEBAS")
        resultados_3 = c.fetchall()

        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM CLASIFICADOR_PARAMETROS")
        resultados_4 = c.fetchall()

        for i in range(len(resultados_2)):
            if (str(pruebas_clasificador_parametros_id_prueba.get()) == str(resultados_2[i][0]) and str(pruebas_clasificador_parametros_id_clasificador.get()) == str(resultados_2[i][1]) and str(pruebas_clasificador_parametros_nombre_parametro.get()) == str(resultados_2[i][2])):
                existe_conjunto = 1

        for i in range(len(resultados)):
            if str(pruebas_clasificador_parametros_id_clasificador.get()) == str(resultados[i][0]):
                existe_clasificador = 1

        for i in range(len(resultados_3)):
            if str(pruebas_clasificador_parametros_id_prueba.get()) == str(resultados_3[i][0]):
                existe_prueba = 1

        for i in range(len(resultados_4)):
            if str(pruebas_clasificador_parametros_nombre_parametro.get()) == str(resultados_4[i][1]):
                existe_parametro = 1

        if existe_conjunto == 0 and existe_clasificador == 1 and existe_prueba == 1 and existe_parametro == 1:
            # Insertamos en la Base de Datos
            insertar_datos(c, conn, "INSERT INTO PRUEBAS_CLASIFICADOR_PARAMETROS (id_prueba, id_clasificador, nombre_parametro, valor) VALUES('" + pruebas_clasificador_parametros_id_prueba.get() + "', '" + pruebas_clasificador_parametros_id_clasificador.get() + "', '" + pruebas_clasificador_parametros_nombre_parametro.get() + "', '" + pruebas_clasificador_parametros_valor.get() + "')")

            # Limpiamos los Text Boxes
            pruebas_clasificador_parametros_id_prueba.delete(0, END)
            pruebas_clasificador_parametros_id_clasificador.delete(0, END)
            pruebas_clasificador_parametros_nombre_parametro.delete(0, END)
            pruebas_clasificador_parametros_valor.delete(0, END)

        elif existe_prueba == 0:
            messagebox.showinfo(message="La prueba introducida no figura en la Base de Datos. Por favor, revisela y vuelva a introducirla.", title="Aviso de Error")

        elif existe_clasificador == 0:
            messagebox.showinfo(message="El clasificador introducido no figura en la Base de Datos. Por favor, reviselo y vuelva a introducirlo.", title="Aviso de Error")

        elif existe_parametro == 0:
            messagebox.showinfo(message="El parametro introducido no figura en la Base de Datos. Por favor, reviselo y vuelva a introducirlo.", title="Aviso de Error")

        elif existe_conjunto == 1:
            messagebox.showinfo(message="El conjunto introducido ya figura con valor en la Base de Datos dentro de ese clasificador. Por favor, reviselo y vuelva a introducirlo.", title="Aviso de Error")

    # Creacion de la funcion Query
    def query_pruebas_clasificador_parametro():
        # Conexion a la Base de Datos
        conn, c = conexion('TFG_DB.db')

        # Consulta a la Base de Datos
        c.execute("SELECT *, oid FROM PRUEBAS_CLASIFICADOR_PARAMETROS ORDER BY id_prueba, id_clasificador")
        resultados = c.fetchall()

        print_resultados = ''
        for resultado in resultados:
            print_resultados += str(resultado[0]) + ' ' + str(resultado[1]) + ' ' + str(resultado[2]) + ' ' + str(resultado[3]) + "\n"

        query_label = Label(window, text=print_resultados)
        query_label.grid(row=7, column=0, columnspan=2)

        # Guardamos los cambios
        conn.commit()

        # Cerramos la conexion a la Base de Datos
        conn.close()

    # Creacion de Text Boxes
    pruebas_clasificador_parametros_id_prueba = Entry(window, width=30)
    pruebas_clasificador_parametros_id_prueba.grid(row=1, column=1, padx=20, pady=2)
    pruebas_clasificador_parametros_id_clasificador = Entry(window, width=30)
    pruebas_clasificador_parametros_id_clasificador.grid(row=2, column=1, padx=20, pady=2)
    pruebas_clasificador_parametros_nombre_parametro = Entry(window, width=30)
    pruebas_clasificador_parametros_nombre_parametro.grid(row=3, column=1, padx=20, pady=2)
    pruebas_clasificador_parametros_valor = Entry(window, width=30)
    pruebas_clasificador_parametros_valor.grid(row=4, column=1, padx=20, pady=2)

    # Creacion de Text Boxes Labels
    pruebas_clasificador_parametros_titulo = Label(window, text="Introduzca los datos del Clasificador", font=("Calibri",12),justify="center")
    pruebas_clasificador_parametros_titulo.grid(row=0, column=0, padx=20, pady=2)
    pruebas_clasificador_parametros_id_prueba_label = Label(window, text="Id_Prueba")
    pruebas_clasificador_parametros_id_prueba_label.grid(row=1, column=0, padx=20, pady=2)
    pruebas_clasificador_parametros_id_clasificador_label = Label(window, text="Id_Clasificador")
    pruebas_clasificador_parametros_id_clasificador_label.grid(row=2, column=0, padx=20, pady=2)
    pruebas_clasificador_parametros_nombre_parametro_label = Label(window, text="Nombre del Parametro")
    pruebas_clasificador_parametros_nombre_parametro_label.grid(row=3, column=0, padx=20, pady=2)
    pruebas_clasificador_parametros_valor_label = Label(window, text="Valor")
    pruebas_clasificador_parametros_valor_label.grid(row=4, column=0, padx=20, pady=2)

    # Creacion de Submit Button
    pruebas_clasificador_parametros_submit_button = Button(window, text="Introducir Valor del Parametro a la Base de Datos", command=submit_pruebas_clasificador_parametro)
    pruebas_clasificador_parametros_submit_button.grid(row = 5, column=0, columnspan=2, padx=20, pady=10, ipadx=100)

    # Creamos un Query Butoon
    clasificador_parametros_query_button = Button(window, text="Mostrar Valor de los Parametros en la Base de Datos", command=query_pruebas_clasificador_parametro)
    clasificador_parametros_query_button.grid(row = 6, column=0, columnspan=2, padx=20, pady=10, ipadx=100)

    window.mainloop()
    