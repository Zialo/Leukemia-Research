from funciones_BBDD_UI_TFG import *

# Funcion Principal

def main():

    # GUI para introducir datos en la tabla Usuarios

    window = Tk()
    window.title('Base de Datos - MAIN')
    window.iconbitmap('Base de Datos/db_icon.ico')
    window.geometry("550x150")

    # Creo el directorio en donde almacenar las consultas
    try:
        os.stat('ConsultasBBDD')
    except:
        os.mkdir('ConsultasBBDD')

    # Creacion de la funcion Submit
    def submit_main():
        if comboExample.current() == -1:
            messagebox.showinfo(message="Por favor, no modifique los valores predeterminados. Repita su seleccion", title="Aviso de Error")

        elif comboExample.current() == 0:
            window.wm_state('iconic')
            tk_consulta()
            
        elif comboExample.current() == 1:
            window.wm_state('iconic')
            tk_usuarios()
            
        elif comboExample.current() == 2:
            window.wm_state('iconic')
            tk_pruebas()
            
        elif comboExample.current() == 3:
            window.wm_state('iconic')
            tk_caracteristicas()
            
        elif comboExample.current() == 4:
            window.wm_state('iconic')
            tk_clasificadores()
            
        elif comboExample.current() == 5:
            window.wm_state('iconic')
            tk_pruebas_caracteristicas()
            
        elif comboExample.current() == 6:
            window.wm_state('iconic')
            tk_pruebas_clasificadores()
            
        elif comboExample.current() == 7:
            window.wm_state('iconic')
            tk_clasificadores_parametros()
            
        elif comboExample.current() == 8:
            window.wm_state('iconic')
            tk_pruebas_clasificadores_parametros()
            
        
    # Creacion de Text Boxes Labels
    titulo = Label(window, text="Base de Datos", font=("Calibri",15),justify="center")
    titulo.grid(row=0, column=1, padx=20, pady=2)
    label = Label(window, text="Escoja una opcion")
    label.grid(row=1, column=0, padx=20, pady=2)

    # Creacion del Selector
    comboExample = ttk.Combobox(window, 
                                values=[
                                        "Realizar una consulta en SQL", 
                                        "Insertar campo en Tabla USUARIOS",
                                        "Insertar campo en Tabla PRUEBAS",
                                        "Insertar campo en Tabla CARACTERISTICAS",
                                        "Insertar campo en Tabla CLASIFICADORES",
                                        "Insertar campo en Tabla PRUEBAS_CARACTERISTICAS",
                                        "Insertar campo en Tabla PRUEBAS_CLASIFICADORES",
                                        "Insertar campo en Tabla CLASIFICADOR_PARAMETROS",
                                        "Insertar campo en Tabla PRUEBAS_CLASIFICADOR_PARAMETROS"])
    comboExample.current(0)
    comboExample.grid(row = 1, column=1, columnspan=2, padx=20, pady=10, ipadx=100)

    # Creacion de Submit Button
    submit_button = Button(window, text="Continuar", command=submit_main)
    submit_button.grid(row = 2, column=2, columnspan=2, padx=10, pady=10, ipadx=30)

    window.mainloop()

main()