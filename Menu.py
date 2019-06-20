import PySimpleGUI as sg
import sopadeletras as Sopa
import constantes as const
import configuracion
import comprobacion as ingreso
from importlib import reload
layout_menu=[[sg.Text('')],
        [sg.Button('JUGAR!')],
        [sg.Text('')],
        [sg.Button('CONFIGURACION')],
        [sg.Text('')],
        [sg.Button('INGRESO DE PALABRAS')],     
        [sg.Text('')],
        [sg.Button('CERRAR')]]

def Main():
    '''Programa Principal. Ejecuta la ventana principal y llama a las funciones
    correspondendientes para la funcion del juego de sopa de letras.
    Funciones:
        configuracion.py
        sopadeletras.py
        comprobacion.py (ingreso de las palabras)
        '''   
    window_menu=sg.Window('Menú',size=(400,450),font='Fixedsys',default_button_element_size=(20,2),
                     auto_size_buttons=False,element_padding=(60,0)).Layout(layout_menu)
    while True:
        event,values=window_menu.Read()
        if event is None or event=='CERRAR':
            window_menu.Close()
            break
        if event=='JUGAR!':
            window_menu.Hide()
            Sopa.Main()
            window_menu.UnHide()
        if event=='CONFIGURACION':
            window_menu.Hide()
            configuracion.Main()
            reload(configuracion)        
            window_menu.UnHide()
        if event=='INGRESO DE PALABRAS':
            ingreso.ingreso_palabra()
            reload(ingreso)
if __name__ =='__main__':
    Main()
            
        

