import Adafruit_DHT

def datos_sensor(pin=17, sensor=Adafruit_DHT.DHT11):
    """ Devuelve un diccionario con la temperatura y humedad """
    dic_datos={"temp":0,"humedad":0}
    dic_datos["humedad"],dic_datos["temp"] = Adafruit_DHT.read_retry(sensor,pin)
    return dic_datos
     
if __name__ == "__main__":
    while True:
        datos = datos_sensor()
        print('Temperatura = {0:0.1f}°C  Humedad = {1:0.1f}%'.format(datos['temp'], datos['humedad']))
        time.sleep(60.0)
