import PySimpleGUI as sg
import constantes as const
import json

sg.SetOptions(background_color='#ffe4b5',button_color=const.COLOR_BOTON,text_element_background_color='#ffe4b5')

def actualizar_archivo(objeto):
        '''Actualiza la configuracion con los datos ingresados en la interface'''
        archivo = open('configuracion.json','w')
        json_datos=json.dumps(objeto)
        archivo.write(json_datos)


lista_cantidad=[]
arcoiris=['azul','verde','rojo','amarillo','violeta','indigo','naranja','celeste']
oficinas=['0','1']
lista_invertir= ['Si','No']
for var in range(11):
    lista_cantidad.append(str(var))
layout=[[sg.Text('Orientacion:'),sg.Radio('Horizontal',"selector1", default=True,background_color='#ffe4b5'),sg.Radio('Vertical', "selector1",background_color='#ffe4b5')],
        [sg.Text('Ayudas:'),sg.Combo(['Ninguna','Definición','Palabras','Ambas'],default_value='Ninguna')],
        [sg.Text('Cantidad de Palabras:')],
        [sg.Text('Verbos'),sg.Combo(lista_cantidad,default_value='0'),
         sg.Text('Adjetivos'),sg.Combo(lista_cantidad,default_value='0'),
         sg.Text('Sustantivos'),sg.Combo(lista_cantidad,default_value='0')],
        [sg.Text('Letras de la sopa'),sg.Radio('Mayuscula','selector2',default=True,background_color='#ffe4b5'),sg.Radio('Minuscula','selector2',background_color='#ffe4b5')],
        [sg.Text('Palabras invertidas'),sg.Combo(lista_invertir,default_value='No')],
        [sg.Text('Colores:')],
        [sg.Text('Verbos:'),sg.Combo(arcoiris,default_value='verde'),
         sg.Text('Adjetivos:'),sg.Combo(arcoiris,default_value='rojo'),
         sg.Text('Sustantivos:'),sg.Combo(arcoiris,default_value='azul')],
        [sg.Text('Oficina'),sg.Combo(oficinas,default_value='0'),sg.Button('Agregar Oficina')],
        [sg.Button('Aplicar')]]
window=sg.Window('Configuraciones',font='Fixedsys',
                 auto_size_buttons=True).Layout(layout)
def comparar_colores(color1,color2,color3):
    '''Comprueba si se ha elegido un mismo color para dos tipos de palabra.
    Retorna falso en caso de ser cierto y True si no se hayan repetidos.'''   
    ok=False
    if color1!=color2 and color2!=color3 and color1!=color3:
        ok=True
    return ok    
def what_color(colorVB,colorJJ,colorNN,dic_colores):
    '''Setea los colores que fueron seleccionados en la interface con sus verdaderos valores sacados de un diccionario.'''    
    return dic_colores[colorVB],dic_colores[colorJJ],dic_colores[colorNN]
    
def Main():
    '''Programa Principa de configuracion.py. Ejecuta el layout de las configuraciones
    y aplica los respectivos cambios al archivo de configuracion.json '''

    dic_colores={'azul':'blue','verde':'green','rojo':'red','amarillo':'yellow','violeta':'violet','naranja':'orange','celeste':'lightblue','indigo':'indigo'}
    while True:
        event,valores=window.Read()
        if event=='Aplicar':
            if comparar_colores(valores[9],valores[10],valores[11]):
                colorVB,colorJJ,colorNN=what_color(valores[9],valores[10],valores[11],dic_colores)
                if valores[0]==False:
                    orientacion = 'Vertical'
                else:
                    orientacion='Horizontal'
                if valores[6]== False:
                    letra='Minuscula'
                else:                    
                    letra='Mayuscula'
                JsonObj=[{'orientacion':orientacion,'ayuda':valores[2],'cant_palabras':{'VB': int(valores[3]),'JJ': int(valores[4]),'NN':int(valores[5])},'tipo_letra':letra,'invertir': valores[8],'colores':{'VB':colorVB,'JJ':colorJJ,'NN':colorNN},'oficina':int(valores[12])}]
                actualizar_archivo(JsonObj)
                break
            else:
                mensaje=[[sg.Text('Por favor ingrese colores distintos para cada tipo de palabra')],
                         [sg.Button('OK')]]
                window_ventana=sg.Window('Colores').Layout(mensaje)
                event,values=window_ventana.Read()
                if event is None or event=='OK':
                    window_ventana.Close()                
        elif event == None:
                 break
    window.Close()
	
if __name__=='__main__':
    Main()
