import PySimpleGUI as sg
import constantes as const
import json
from funciones import leer_archivo

def actualizar_archivo(objeto):
        '''Actualiza la configuracion con los datos ingresados en la interface'''
        archivo = open('json files/configuracion.json','w')
        json_datos=json.dumps(objeto, indent=4)
        archivo.write(json_datos)
        archivo.close
       
def conseguir_color(clave,config):
    dic_colores={'blue':'azul','green':'verde','red':'rojo','yellow':'amarillo','violet':'violeta','orange':'naranja','lightblue':'celeste','indigo':'indigo'}
    return dic_colores[config[clave]]
def conseguir_booleano(valor, config):
        OK=False
        if config==valor:
                OK=True
        return OK
def crear_layout(colores):
        config=leer_archivo('json files/configuracion.json')[0]
        lista_cantidad=[]
        arcoiris=['azul','verde','rojo','amarillo','violeta','indigo','naranja','celeste']
        oficinas=list(leer_archivo("json files/datos-oficinas.json").keys())
        lista_invertir= ['Si','No']
        for var in range(11):
            lista_cantidad.append(str(var))
        layout=[[sg.Text('Orientacion:'),sg.Radio('Horizontal',"selector1", default=conseguir_booleano('Horizontal',config['orientacion']),background_color=colores["COLOR_FONDO"]),sg.Radio('Vertical', "selector1",default=conseguir_booleano('Vertical',config['orientacion']),background_color=colores["COLOR_FONDO"])],
                [sg.Text('Ayudas:'),sg.Combo(['Ninguna','Definición','Palabras','Ambas'],default_value=config["ayuda"])],
                [sg.Text('Cantidad de Palabras:')],
                [sg.Text('Verbos'),sg.Combo(lista_cantidad,default_value=str(config["cant_palabras"]["VB"])),
                 sg.Text('Adjetivos'),sg.Combo(lista_cantidad,default_value=str(config["cant_palabras"]["JJ"])),
                 sg.Text('Sustantivos'),sg.Combo(lista_cantidad,default_value=str(config["cant_palabras"]["NN"]))],
                [sg.Text('Letras de la sopa'),sg.Radio('Mayuscula','selector2',default=conseguir_booleano('Mayuscula',config['tipo_letra']),background_color=colores["COLOR_FONDO"]),sg.Radio('Minuscula','selector2',default=conseguir_booleano('Minuscula',config['tipo_letra']),background_color=colores["COLOR_FONDO"])],
                [sg.Text('Palabras invertidas'),sg.Combo(lista_invertir,default_value=config["invertir"])],
                [sg.Text('Colores:')],
                [sg.Text('Verbos:'),sg.Combo(arcoiris,default_value=conseguir_color('VB',config['colores'])),
                 sg.Text('Adjetivos:'),sg.Combo(arcoiris,default_value=conseguir_color('JJ',config['colores'])),
                 sg.Text('Sustantivos:'),sg.Combo(arcoiris,default_value=conseguir_color('NN',config['colores']))],
                [sg.Text('Oficina'),sg.Combo(oficinas,default_value=config["oficina"])],
                [sg.Button('Aplicar'),sg.Button('Cancelar')]]
        return layout

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
    colores=leer_archivo('json files/colores.json')    
    sg.SetOptions(background_color=colores["COLOR_FONDO"],button_color=colores["COLOR_BOTON"], text_element_background_color=colores["COLOR_FONDO"])    
    '''Programa Principa de configuracion.py. Ejecuta el layout de las configuraciones
    y aplica los respectivos cambios al archivo de configuracion.json '''
    window=sg.Window('Configuraciones',font='Fixedsys',auto_size_buttons=True).Layout(crear_layout(colores))
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
                JsonObj=[{'orientacion':orientacion,'ayuda':valores[2],'cant_palabras':{'VB': int(valores[3]),'JJ': int(valores[4]),'NN':int(valores[5])},'tipo_letra':letra,'invertir': valores[8],'colores':{'VB':colorVB,'JJ':colorJJ,'NN':colorNN},'oficina':valores[12]}]
                actualizar_archivo(JsonObj)
                break
            else:
                mensaje=[[sg.Text('Por favor ingrese colores distintos para cada tipo de palabra')],
                         [sg.Button('OK')]]
                window_ventana=sg.Window('Colores').Layout(mensaje)
                event,values=window_ventana.Read()
                if event is None or event=='OK':
                    window_ventana.Close()                
        elif event == None or event=='Cancelar':
                 break
    window.Close()
	
if __name__=='__main__':
    Main()
