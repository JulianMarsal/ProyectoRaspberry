import PySimpleGUI as sg
import sopadeletras as Sopa
import constantes as const
import configuracion
import comprobacion as ingreso
from importlib import reload
import json
from funciones import leer_archivo

def promedio_temperatura():
    oficinas=leer_archivo("json files/datos-oficinas.json")
    config=leer_archivo("json files/configuracion.json")[0]
    oficina_promedio=oficinas[config['oficina']]
    temperaturas=0
    cant_temperaturas=0
    for var in oficina_promedio:
        temperaturas+=var["temp"]
        cant_temperaturas+=1
    return temperaturas / cant_temperaturas

def look_and_feel():
    temperatura=promedio_temperatura()
    foto= 'images/logo.png'
    if temperatura<10:
        color="#291E9C"
        color_boton=["white","#525AFE"]
    elif 10<temperatura<20:
        color="#9FD9DA"
        color_boton=["white","#4E8498"]
    elif 20<temperatura<27:
        color="#FBB40D"
        color_boton=["black","#FACA3C"]
    elif temperatura>27:
        color="#E6402A"
        color_boton=["white","#C82610"]
    colores=leer_archivo("json files/colores.json")
    colores['COLOR_FONDO']=color
    colores['COLOR_BOTON']=color_boton
    colores['COLOR_TEXTO'][1]=color
    archivo=open('json files/colores.json','w')
    objeto=json.dumps(colores,indent=4)
    archivo.write(objeto)
    archivo.close
    return foto, color,color_boton

def Main():
    foto,color,color_boton=look_and_feel()
    color_boton=color_boton
    sg.SetOptions(background_color=color,button_color=color_boton, text_element_background_color=color) 
    layout_menu=[[sg.Text('')],
            [sg.Button('JUGAR!')],
            [sg.Text('')],
            [sg.Button('CONFIGURACION')],
            [sg.Text('')],
            [sg.Button('INGRESO DE PALABRAS')],     
            [sg.Text('')],
            [sg.Button('CERRAR')],
            [sg.Image(filename=foto,background_color=color)]]     
    '''Programa Principal. Ejecuta la ventana principal y llama a las funciones
    correspondendientes para la funcion del juego de sopa de letras.
    Funciones:
        configuracion.py
        sopadeletras.py
        comprobacion.py (ingreso de las palabras)
        '''
    window_menu=sg.Window('Menú',size=(400,500),font='Fixedsys',default_button_element_size=(20,2),
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
            window_menu.UnHide()
        if event=='INGRESO DE PALABRAS':
            ingreso.main()
if __name__ =='__main__':
    Main()
            
        

