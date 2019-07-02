import PySimpleGUI as sg
import random as rd
import string
import constantes as const
import json


sg.SetOptions(background_color='#ffe4b5',button_color=const.COLOR_BOTON,text_element_background_color='#ffe4b5')

def agregar_fila(layout, m, cant):
    '''Agrega una fila de letras random a la sopa de letras'''
    lista=[]
    for x in range(m):
        lista.append(sg.ReadButton(rd.choice(string.ascii_letters).upper(),size=(1,1),font='Bold',key=(x,cant)))
    layout.append(lista)
    return layout

def agregar_columna(layout, long, cant):
    '''Agrega un columna de letras random a la sopa de letras'''
    for i in range(long):
        layout[i].append(sg.ReadButton(rd.choice(string.ascii_letters).upper(),size=(1,1),font='Bold',key=(cant,i)))
    return layout

def crear_cuadrado(m, tipo_let):
    '''Crea un cuadrado de letras random segun la longitud de la palabra mas larga'''
    layout=[]
    if (tipo_let =='Mayuscula'):
        for i in range(m):
            lista=[]
            for x in range(m):
                lista.append(sg.ReadButton(rd.choice(string.ascii_letters).upper(),size=(1,1),font='Bold',key=(x,i)))
            layout.append(lista)
    elif (tipo_let =='Minuscula'):
        for i in range(m):
            lista=[]
            for x in range(m):
                lista.append(sg.ReadButton(rd.choice(string.ascii_letters).lower(),size=(1,1),font='Bold',key=(x,i)))
            layout.append(lista)
        
    return layout      

def invertido(palabra):
    '''Si se eligio la configuracion de palabras invertidas se invierte de forma random las palabras a agregar'''
    invertir=rd.randrange(2)
    if invertir:
        palabra=palabra[::-1]
    return palabra

def agregar_horizontal(layout,dic_palabras,invertir,longitud):
    '''Agrega las palabras seleccionadas a la sopa de letras de forma horizontal'''
    cant=longitud-1
    coord_palabras={'VB':[],'JJ':[],'NN':[]} 
    lista_filas=list(range(longitud))
    dic_filas={}
    for fila in range(longitud):
        dic_filas[fila]=[]
    for llave in dic_palabras:    
        for palabra in dic_palabras[llave]:
            while True:
                try:
                    fila=rd.choice(lista_filas)
                    mover=(longitud-len(palabra))+1
                    columna=rd.randrange(mover)
                    if dic_filas[fila]:
                        pri=dic_filas[fila][0][0]
                        ult=dic_filas[fila][-1][0]
                        if pri>=len(palabra):
                            columna=rd.randrange(pri-len(palabra)+1)
                            break
                        elif(longitud-1)-ult==len(palabra):
                            columna=ult+1
                            break
                        elif (longitud-1)-ult>len(palabra):
                            pos=ult+1
                            columna=rd.randrange(pos,pos+((longitud-1)-(pos-1)-len(palabra)))
                            break
                        else:
                            lista_filas.remove(fila) 
                    else:
                        break                 
                except:
                    cant+=1
                    layout = agregar_fila(layout,longitud,cant)
                    lista_filas.append(cant)
                    dic_filas[cant]=[]
            if(invertir==True):
                palabra=invertido(palabra)
            for caracter in palabra:
                layout[fila][columna]=sg.ReadButton(caracter,size=(1,1),font='Bold',key=(columna,fila))
                dic_filas[fila].append((columna,fila))
                coord_palabras[llave].append((columna,fila))
                columna+=1
    return(layout,coord_palabras)        

def agregar_vertical(layout,dic_palabras,invertir,longitud):
    '''Agrega las palabras seleccionadas a la sopa de letras de forma vertical'''
    cant=longitud-1
    dic_columnas={}   #tiene como clave la columna, y como valor las coordenadas de la palabra de la columna (si es que tiene)
    coord_palabras={'VB':[],'JJ':[],'NN':[]}    
    for var in range(longitud):
        dic_columnas[var]=[]
    lista_columnas=list(range(longitud))
    for llave in dic_palabras:
        for palabra in dic_palabras[llave]:
            while True:
                try:
                    columna=rd.choice(lista_columnas)
                    mover=(longitud-len(palabra))+1
                    fila=rd.randrange(mover)
                    if dic_columnas[columna]:   #si hay algo en la lista(osea si ya hay una palabra en la columna) da true, sino (listavacia) da false
                        pri=dic_columnas[columna][0][1]
                        ult=dic_columnas[columna][-1][1]
                        if pri>=len(palabra):
                            fila=rd.randrange(pri-len(palabra)+1)  #la variable fila es desde donde empezas a escribrir la palabra nueva
                            break
                        elif(longitud-1)-ult==len(palabra): 
                                fila=ult+1
                                break
                        elif ((longitud-1)-ult>len(palabra)):
                            ult+=1
                            fila=rd.randrange(ult,ult+(((longitud-1)-(ult-1))-len(palabra)))
                            break
                        else:
                            lista_columnas.remove(columna)  #no hay espacio libre en la columna, la elimina de disponibles
                    else:
                        break  #no hay nada en esa columna, todos los espacios libres
                except(IndexError):  #cuando la lista de comlumnas está vacia, no hay lugar para agregar nada
                    cant+=1
                    layout = agregar_columna(layout,longitud,cant)
                    lista_columnas.append(cant)
                    dic_columnas[cant]=[]
            if(invertir==True):
                palabra=invertido(palabra)   
            for caracter in palabra:
                layout[fila][columna]=sg.ReadButton(caracter,size=(1,1),font='Bold',key=(columna,fila))
                dic_columnas[columna].append((columna,fila))
                coord_palabras[llave].append((columna,fila))
                fila+=1
    return(layout,coord_palabras)

def agregar_botones(layout,lista_pal,colores,ayuda, dic_pal, palabras,cantidad):
    '''Agrega los botones necesarios para la funcion de la sopa junto con las ayudas pedidas'''
    layout.append([sg.Button('Verbos',button_color=('white',colores['VB'])),sg.Button('Adjetivos', button_color=('white', colores['JJ'])),
                   sg.Button('Sustantivos', button_color=('white', colores['NN']))])
    if (ayuda == 'Ninguna'):
        layout.append([sg.Text('Cantidad verbos:'+str(cantidad['VB'])),sg.Text('Cantidad adjetivos:'+ str(cantidad['JJ'])),sg.Text('Cantidad sustantivos:'+ str(cantidad['NN']))])    
    if (ayuda == 'Ambas' or ayuda=='Palabras'):
        layout.append([sg.Text('Palabras:')])
        layout.append([sg.Multiline(lista_pal)])
    if (ayuda=='Ambas' or ayuda=='Definición'):
        layout.append([sg.Button('Mostrar definiciones')])
    layout.append([sg.Button('Borrar Tablero'),sg.Button('Borrar boton')])
    layout.append([sg.Button('Volver al menú'),sg.Button('Listo!'),sg.Button ('   ',size=(1,1),key='color_actual')])
    return layout

def crear_sopa(palabras_todas, config):
    '''Funcion que crea la sopa de letras segun las configuraciones del archivo configuracion.json'''
    lista_palabras=[]
    diccionario_palabras={'VB':[],'JJ':[],'NN':[]}
    for x in config[0]['cant_palabras']:
        claves=list(palabras_todas[0][x].keys())
        veces_del_random=config[0]['cant_palabras'][x]
        if veces_del_random>len(claves):
            veces_del_random=len(claves)
            config[0]['cant_palabras'][x]=len(claves)
        for var in range(veces_del_random):
           pal=rd.choice(claves)
           while(pal in lista_palabras):
                pal=rd.choice(claves)
           lista_palabras.append(pal)     
           if (config[0]['tipo_letra'] =='Mayuscula'):
                    pal=pal.upper()    #se agregan todas en minuscula en el json
           diccionario_palabras[x].append(pal)         
    longitud=max(len(elem) for elem in lista_palabras)+1
    layout=crear_cuadrado(longitud, config[0]['tipo_letra'])
    if config[0]['orientacion']=='Horizontal':
        layout,coord_palabras= agregar_horizontal(layout,diccionario_palabras,config[0]['invertir'],longitud)
    elif config[0]['orientacion']=='Vertical':
        layout,coord_palabras= agregar_vertical(layout,diccionario_palabras,config[0]['invertir'],longitud)
    return agregar_botones(layout,lista_palabras,config[0]['colores'],config[0]['ayuda'], diccionario_palabras, palabras_todas,config[0]['cant_palabras']),coord_palabras, diccionario_palabras

def comprobar(pintadas, coord_correctas):
    '''Comprueba si las casillas fueron marcadas correctamente'''
    OK=[]
## Este if pregunta si el elemento de la lista en pintadas esta en la lista en coordenadas,si pintadas no esta vacia,
## si hay la misma cantidad de elementos en pintadas y coordenadas.   
    for x in coord_correctas:
        if all(map(lambda elem: False if not elem in coord_correctas[x] else True,pintadas[x]))and all([True if len(coord_correctas[elem])==len(pintadas[elem]) else False for elem in coord_correctas]):
            OK.append(True)
        else:
            OK.append(False)            
    if all(OK): #all devuelve true si en el iterable pasado como argumento no hay ningun false. 
        layout=[[sg.Text('Lo haz logrado!',font='Bold')],[sg.OK()]]
    else:
        layout=[[sg.Text('No haz marcado con los colores correctos o te faltaron marcar letras',font='Bold')],[sg.OK()]]
    window=sg.Window('Resultado').Layout(layout)
    button,valor=window.Read()
    if button=='OK'or None:
        window.Close()
        
def comparar(coordenada,ingresado,correcta,clave1,clave2):
    '''Comprueba si la coordenada ingresado no ha sido ingresada en otra clasificacion. En caso afirmativo la elimina de esa
    clasificacion y la agrega a la que corresponde el color con el que ha sido marcado.'''
    if coordenada in ingresado[clave1]:
        ingresado[clave1].remove(coordenada)
    if coordenada in ingresado[clave2]:
        ingresado[clave2].remove(coordenada)
    if not coordenada in ingresado[correcta]:
        ingresado[correcta].append(coordenada)    
        
def abrir_jsonPalabras():
    '''Abre el archivo palabras.json y devuelve sus valores'''
    archivo =open ('palabras.json', 'r')
    palabras = json.load(archivo)
    return palabras  #Lista con 1 diccionario ([{'VB':{'correr':asds,'caminar':abfu},'JJ':{'hermoso':bghuhuf,'horrible':huhus},'NN':{}}])
    
def abrir_jsonConfiguracion():
    '''Abre el archivo configuracion.json y devuelve sus valores'''
    archivo =open('configuracion.json', 'r')
    config= json.load(archivo)     #lista de diccionario [{'ayuda':'Palabras','colores':{'VB':'rojo','JJ':'verde','NN':'amarillo'},'orientacion':'vertical','tipo_letra':'mayuscula','cant_palabras':{'VB':2,'JJ':3,'NN':4},'oficina':1,'invertir':True}]
    return config

def tabla_definiciones(palabras_todas,palabras_sopa):
	lis_definiciones=[]
    caracteres=['1','2','3','4','5','6','7','8','9','0','{','}','[',']']
	for x in palabras_sopa:
		for palabra in palabras_sopa[x]:
			definicion=palabras_todas[0][x][palabra.lower()]
            for elem in caracteres:
                definicion.strip(elem)
			lis_definiciones.append(definicion)
			lis_definiciones.append('\n')
	header_list=[]
	layout2 = [[sg.Table(values=lis_definiciones,
                            headings=header_list)]]
	window2 = sg.Window('Definiciones').Layout(layout2)
	event,valores=window2.Read()

def Main():
    '''Programa Principal de Sopa de letras.
    Se encarga de la creacion de la sopa de letras y del ingreso de las coordenadas de las casillas marcadas.
    Se encarga de la comprobacion de las casillas marcadas y de volver al menu.'''
    palabras = abrir_jsonPalabras()
    config= abrir_jsonConfiguracion()
    layout,coor, palabras_sopa=crear_sopa(palabras,config)
    #aca poner color segun oficina
    window=sg.Window('Sopa de letras',font='Courier').Layout(layout)
    ingresados={'VB':[],'JJ':[],'NN':[]}
    color=const.COLOR_BOTON
    while True:
        event,values=window.Read()
        if(event is None or event=='Volver al menú'):
            break
        elif type(event)==tuple:
            if(color[1]==config[0]['colores']['VB']):
                comparar(event,ingresados,'VB','JJ','NN')            
            elif(color[1]==config[0]['colores']['JJ']):
                comparar(event,ingresados,'JJ','VB','NN')
            elif(color[1]==config[0]['colores']['NN']):
                comparar(event,ingresados,'NN','JJ','VB')
            elif(color==const.COLOR_BOTON):
                for var in ingresados:
                    if event in ingresados[var]:
                        ingresados[var].remove(event)                    
            window.FindElement(event).Update(button_color=color)
        elif(event=='Adjetivos'):
            color=('white',config[0]['colores']['JJ'])
            window.FindElement('color_actual').Update(button_color=color)
        elif(event=='Sustantivos'):
            color=('white',config[0]['colores']['NN'])
            window.FindElement('color_actual').Update(button_color=color)
        elif(event=='Verbos'):
            color=('white',config[0]['colores']['VB'])
            window.FindElement('color_actual').Update(button_color=color)
        elif (event == 'Mostrar definiciones'):
            tabla_definiciones(palabras, palabras_sopa)
        elif(event=='Borrar boton'):
            color=const.COLOR_BOTON
            window.FindElement('color_actual').Update(button_color=color)
        elif(event=='Borrar Tablero'):
            for llave in ingresados:
                if ingresados[llave]:
                    for var in ingresados[llave]:
                        window.FindElement(var).Update(button_color=const.COLOR_BOTON)
            for llave in ingresados:
                ingresados[llave].clear()            
        elif(event=='Listo!'):
            comprobar(ingresados, coor)
    window.Close()
if __name__=='__main__':
    Main()

