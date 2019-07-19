import json
def leer_archivo(nombre_archivo):
        archivo = open (nombre_archivo,'r')
        json_datos=json.load(archivo)
        archivo.close
        return json_datos
