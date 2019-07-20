import PySimpleGUI as sg
import pattern.es as pat
from pattern.web import Wiktionary as wik
import constantes as const
import string as st
import json
from funciones import leer_archivo

def mostrar_palabras():
    palabras=leer_archivo('json files/palabras.json')[0]
    lista_palabras=[]
    for var in palabras:
        lista_palabras.extend(list(palabras[var].keys()))
    layout=[[sg.Multiline(lista_palabras,size=(40,12),disabled=True)],[sg.Button('Cerrar')]]
    window=sg.Window('json files/Palabras').Layout(layout)
    event,values=window.Read()
    window.Close()    

def mostrar_reporte():
    '''Abre los diferentes archivos.txt de reporte y los junta en un multiline quitando el contenido redundante'''
    reporte= open('report files/reporte_wikcionario','r')
    lista_reporte=(reporte.read()+'\n\n'+ '-------------------------------------------------------------------------------------------------------------------------------------------------' + '-------------------------------------------------------------------------------------------------------------------------------------------------------'+'\n\n\n') 
    reporte.close() 
    reporte= open('report files/reporte_pattern','r')
    lista_reporte+=(reporte.read()+'\n\n'+ '-------------------------------------------------------------------------------------------------------------------------------------------------' + '-------------------------------------------------------------------------------------------------------------------------------------------------------'+'\n\n\n')
    lista_reporte=lista_reporte.replace("No existe la palabra en el wiktionario. Se tomara la clasificacion de pattern si existe.", " ")
    reporte.close()
# Descomentar en caso de querer incluir el reporte de palabras inexistentes en ambos buscadores
#   reporte= open('report files/reporte_wikcionario_pattern','r')
#   lista_reporte+=(reporte.read()+'\n\n'+ '-------------------------------------------------------------------------------------------------------------------------------------------------' + '-------------------------------------------------------------------------------------------------------------------------------------------------------'+'\n\n\n')
#   lista_reporte=lista_reporte.replace("La palabra no se encuentra en wikcionario y no clasifica como verbo, adjetivo o sustantivo en pattern.", " ")
#   reporte.close()      
    layout=[[sg.Multiline(lista_reporte,size=(85,15),disabled=True)],[sg.Button('Cerrar')]]
    window=sg.Window('report files/reporte').Layout(layout)
    event,values=window.Read()
    window.Close()

def actualizar_archivoPal(objeto):
    '''Recibe un diccionario con datos de palabras y sus definiciones y actualiza el archivo palabras.json'''
    datos_archivo=leer_archivo('json files/palabras.json')
    for x in objeto[0]:
        for palabra in objeto[0][x]:
            datos_archivo[0][x][palabra]=objeto[0][x][palabra]
    nuevos=json.dumps(datos_archivo, indent=4)
    archivo=open('json files/palabras.json','w')
    archivo.write(nuevos)
    archivo.close

def eliminar(palabra):
    '''Recibe una palabra y la elimina del archivo palabras.json'''
    palabra=palabra.lower()    
    datos=leer_archivo('json files/palabras.json')
    for x in datos[0]:
         llaves=list(datos[0][x].keys())
         if palabra in llaves:
                 del datos[0][x][palabra]
                 mensaje =' Se ha eliminado con exito'
                 break
         else:
            mensaje= 'La palabra no se encuentra en el archivo'
    nuevos=json.dumps(datos, indent=4)
    archivo=open('json files/palabras.json','w')
    archivo.write(nuevos)
    archivo.close
    layout=[[sg.Text(mensaje,font='Courier')],
            [sg.Button('Aceptar')]]
    window=sg.Window('Eliminado').Layout(layout)
    while True:
        event,values=window.Read()
        if event==None or event=='Aceptar':
            break
    window.Close()
    

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
            clasificacion=tag
            for var in const.TAGS_FUNCIONAL:
                if const.TAGS_FUNCIONAL[var] in texto:
                    tag=var
                    break
            for x in range(len(secciones)):
                if const.TAGS_FUNCIONAL[tag] in secciones[x].title:
                    indice=x
                    break
            #Reportando a pattern
            lectura_pattern=open("report files/reporte_pattern",'r')    
            if not palabra in (' ').join(lectura_pattern.readlines()):    
                reporte_pattern=open("report files/reporte_pattern",'a')
                reporte="<<"+palabra+">> La clasificacion de pattern y wiktionary difieren. Pattern="+clasificacion+". Wiktionary="+secciones[indice].title+". \n"
                reporte_pattern.write(reporte)
                reporte_pattern.close()
            lectura_pattern.close()    
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
                lectura_wikcionario=open("report files/reporte_wikcionario",'r')
                if not palabra in (' ').join(lectura_wikcionario.readlines()):
                    reporte_wikcionario=open("report files/reporte_wikcionario",'a')
                    reporte="<<"+palabra+">> No existe la palabra en el wiktionario. Se tomara la clasificacion de pattern si existe."
                    reporte_wikcionario.write(reporte)
                    reporte_wikcionario.close()
                lectura_wikcionario.close()
                if tag=='NN':
                    entra=comprobar_sustantivo(palabra)
                if entra and (tag=='VB' or tag=='JJ'or tag=='NN'):    
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
                            descrip=values
                            window.Close()
                else:
                    #Reportando a wikcionario y pattern
                    lectura_wik_pat=open("report files/reporte_wikcionario_pattern",'r')
                    if not palabra in (' ').join(lectura_wik_pat.readlines()):
                        reporte_wikcionario_pattern=open("report files/reporte_wikcionario_pattern",'a')
                        if entra:
                            reporte="<<"+palabra+">> La palabra no se encuentra en wikcionario y no clasifica como verbo, adjetivo o sustantivo en pattern.\n"
                        else:
                            reporte="<<"+palabra+">> La palabra no se encuentra en wikcionario ni en pattern.\n"
                        reporte_wikcionario_pattern.write(reporte)
                        reporte_wikcionario_pattern.close()
                    lectura_wik_pat.close()     
                    entra=False
                    layout=[[sg.Text('No se encuentra la palabra en wikcionario ni en pattern. Se incluirá en un reporte.')],
                            [sg.OK()]]
                    window=sg.Window('No se encuentra').Layout(layout)
                    event,values=window.Read()
                    if event is None or event=='OK':
                            window.Close()       
    if entra:
        jsonObj[0][tag][palabra]=descrip
    return jsonObj

def main():
    colores=leer_archivo('json files/colores.json')
    sg.SetOptions(background_color=colores["COLOR_FONDO"],text_color='white',button_color=colores["COLOR_BOTON"], text_element_background_color=colores["COLOR_FONDO"])    
    '''Programa Principal de comprobacion.py.
    Realiza el ingreso/eliminacion de palabras al archivo palabras.json llamando a las respectivas funciones declaradas en comprobacion.py'''
    layout=[[sg.Text('¡Bienvenido a la sección de ingreso de palabras!')],
        [sg.Text('Ingrese la palabra a agregar/eliminar. Puede tardar en comprobar la palabra en internet.')],
        [sg.Input()],
        [sg.Text('<<Una palabra por vez. Con acentuación incluída>>.<<Máximo de longitud:10 >> ', text_color='red')],
        [sg.Button('Agregar'),sg.Button('Eliminar'),sg.Button('Mostrar Palabras'),sg.Button('Mostrar Reporte')],
        [sg.Button('Terminar')]]
    window= sg.Window('Ingreso de palabras').Layout(layout)
    while True:
        event,values=window.Read()
        if event == None or event=='Terminar':
            break
        elif event == 'Agregar' and values !=['']:
            jsonObj=[{"VB":{},"JJ":{},"NN":{}}]
            tipo=verificacion_palabra(values[0],jsonObj)
            actualizar_archivoPal(jsonObj)
        elif event=='Eliminar':
            eliminar(values[0]) 
        elif event == 'Mostrar Palabras':
            mostrar_palabras()   
        elif event == 'Mostrar Reporte':
            mostrar_reporte()
            
    window.Close()  
    
    
if __name__=='__main__':
    main()

