import PySimpleGUI as sg
import pattern.es as pat
from pattern.web import Wiktionary as wik
import constantes as const
import string as st
import json 

sg.SetOptions(background_color='#ffe4b5',button_color=const.COLOR_BOTON,text_element_background_color='#ffe4b5')

def abrir_archivo():
    '''Abre el archivo de palabras.json y retorna sus valores'''
    archivo = open('palabras.json','r')
    datos=json.load(archivo)
    archivo.close
    return datos

def actualizar_archivoPal(objeto):
    '''Recibe un diccionario con datos de palabras y sus definiciones y actualiza el archivo palabras.json'''
    datos_archivo=abrir_archivo()
    for x in objeto[0]:
        for palabra in objeto[0][x]:
            datos_archivo[0][x][palabra]=objeto[0][x][palabra]
    nuevos=json.dumps(datos_archivo)
    archivo=open('palabras.json','w')
    archivo.write(nuevos)
    archivo.close
def eliminar(palabra):
    '''Recibe una palabra y la elimina del archivo palabras.json'''
    palabra=palabra.lower()    
    datos=abrir_archivo()
    for x in datos[0]:
         llaves=list(datos[0][x].keys())
         if palabra in llaves:
                 del datos[0][x][palabra]
                 break
    nuevos=json.dumps(datos)
    archivo=open('palabras.json','w')
    archivo.write(nuevos)
    archivo.close

def comprobar_sustantivo(palabra):
    '''Comprueba si existe el sustantivo pasado por parametro ya que pattern.es
    manda como sustantivos hasta las palabras inexistentes'''
    es_sustantivo = False    
    if (palabra in pat.spelling) or (palabra in pat.lexicon):
        es_sustantivo = True
    return es_sustantivo

def verificacion_palabra(palabra,jsonObj):
    '''Verifica que tipo de clasificacion tiene la palabra en pattern.es y en wikcionario.
Realiza reportes si:
  *No se encuentra la palabra en wikcionario
  *No se encuentra la palabra en wikcionario ni en pattern.es
  *No coinciden las clasificaciones de wikcionario y pattern.es'''
    entra=True
    try:
        palabra=palabra.lower()
        tipo_pat=pat.tag(palabra)
        tag=tipo_pat[0][1][0:2]
        engine=wik(language='es')
        articulo=engine.article(palabra)
        secciones=articulo.sections
        texto=articulo.plaintext()
        if const.TAGS_FUNCIONAL[tag] in texto:
            for x in range(len(secciones)):
                if const.TAGS_FUNCIONAL[tag] in secciones[x].title:
                    indice=x
                    break
        else:
            for var in const.TAGS_FUNCIONAL:
                if const.TAGS_FUNCIONAL[var] in texto:
                    tag=var
                    break
            for x in range(len(secciones)):
                if const.TAGS_FUNCIONAL[tag] in secciones[x].title:
                    indice=x
                    break
            #Reportando a pattern 
            reporte_pattern=open("reporte_pattern",'a')
            reporte_pattern.write(palabra)
            reporte_pattern.close()
        descripciones= secciones[indice].plaintext()
        lista_descripciones=descripciones.split('\n')
        desc=[]
        for var in lista_descripciones:
            for n in range(10):
                if str(n) in var:
                    desc.append(var)
                    break
        layout=[[sg.Text('Por favor seleccione una de las descripciones para la palabra.')],
            [sg.Text('Utilice las flechas arriba/abajo para seleccionar en caso de ser muy larga la descripcion')],
            [sg.Combo(desc,default_value=desc[0])],
            [sg.Button('Aceptar')]]
        window=sg.Window('Elija descripcion').Layout(layout)
        while True:
            event,values=window.Read()
            if event is None or event=='Aceptar':
                descrip=values
                break
        window.Close()
    except AttributeError:
                #Reportando a wikcionario
                reporte_wikcionario=open("reporte_wikcionario",'a')
                reporte_wikcionario.write(palabra)
                reporte_wikcionario.close()
                if tag=='NN':
                    entra=comprobar_sustantivo(palabra)
                if entra:    
                    texto1='No existe un articulo en wikcionario de la palabra <<'+palabra+'>>.'
                    if 'JJ' in tag:
                            texto2='Segun el modulo <<pattern.es>> la palabra ingresada es un adjetivo.'
                    elif 'NN' in tag:
                            texto2='Segun el modulo <<pattern.es>> la palabra ingresada es un sustantivo.'
                    elif 'VB' in tag:
                            texto2='Segun el modulo <<pattern.es>> la palabra ingresada es un verbo.'
                    layout=[[sg.Text(texto1)],
                            [sg.Text(texto2)],
                            [sg.Text('Ingrese una descripcion para dicha palabra:'),sg.Input()],
                            [sg.OK()]]
                    window=sg.Window('Descripcion').Layout(layout)
                    event,values=window.Read()
                    if event is None or event=='OK':
                            descrip=values[0]
                            window.Close()
                else:
                    reporte_wikcionario_pattern=open("reporte_wikcionario_pattern",'a')
                    reporte_wikcionario_pattern.write(palabra)
                    reporte_wikcionario_pattern.close()
    if entra:
        jsonObj[0][tag][palabra]=descrip
    return jsonObj

def ingreso_palabra():
    '''Programa Principal de comprobacion.py.
    Realiza el ingreso/eliminacion de palabras al archivo palabras.json llamando a las respectivas funciones declaradas en comprobacion.py'''
    layout=[[sg.Text('¡Bienvenido a la sección de ingreso de palabras!')],
        [sg.Text('Ingrese la palabra a agregar/eliminar. Puede tardar en comprobar la palabra en internet.')],
        [sg.Input()],
        [sg.Text('<<Una palabra por vez. Con acentuación incluída>>.<<Máximo de longitud:10 >> ', text_color='red')],
        [sg.Button('Agregar'),sg.Button('Eliminar')],
        [sg.Button('Listo')]]
    window= sg.Window('Ingreso de palabras').Layout(layout)
    jsonObj=[{"VB":{},"JJ":{},"NN":{}}]
    while True:
        event,values=window.Read()
        if event == None:
            break
        elif event == 'Agregar' and values !=['']:
            tipo=verificacion_palabra(values[0],jsonObj)
        elif event=='Eliminar':
            eliminar(values[0])    
        elif event == 'Listo':
            actualizar_archivoPal(jsonObj)
            break
    window.Close()  
    
    
if __name__=='__main__':
    ingreso_palabra()
