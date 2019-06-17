import PySimpleGUI as sg
import pattern.es as pat
from pattern.web import Wiktionary as wik
prueba=['mirar','miedo','llorando','escribir','parcial','horrendo','casa','tranquilo']
def ingreso_palabra(palabra,tipo, tags={'NN':'ustantiv','VB':'erb','JJ':'djetiv'}):
    try:
        tipo_pat=pat.tag(palabra)
        tag=tipo_pat[0][1][0:2]
        engine=wik(language='es')
        articulo=engine.article(palabra)
        secciones=articulo.sections
        texto=articulo.plaintext()
        print(tag)
        if tags[tag] in texto:
            tipo[tag].append(tipo_pat[0][0])
            for x in range(len(secciones)):
                if tags[tag] in secciones[x].title:
                    indice=x
                    break
            descripciones= secciones[indice].plaintext()
            print(descripciones)
        else:
            for var in tags:
                if tags[var] in texto:
                    tag=var
                    break
            if tags[var] in texto:
                tipo[tag].append(tipo_pat[0][0])
                for x in range(len(secciones)):
                    if tags[tag] in secciones[x].title:
                        indice=x
                        break
                descripciones= secciones[indice].plaintext()
                print(descripciones)
                #Esta mal pattern, reportarlo
    except AttributeError:
        tipo[tag].append(palabra)
        print('No existe un articulo de wikcionario de la palabra <<',palabra,'>>')
        print('La palabra ingresado es un',tags[tag],'segun pattern, ingrese una descripcion para dicha palabra.')        
    return tipo     
tipo={'VB':[],'NN':[],'JJ':[]}
ingreso_palabra('felices',tipo)
print(tipo)    









    
##    if tipo_pat[0][1][0:2]=='NN' and 'Sustantivo' in texto:
##        sustantivos.append(tipo_pat[0][0])    
##    elif tipo_pat[0][1][0:2]=='VB' and 'Verbo' in texto:
##        verbos.append(tipo_pat[0][0])
##    elif tipo_pat[0][1][0:2]=='JJ'and 'Adjetivo' in texto:
##        adjetivos.append(tipo_pat[0][0])    
