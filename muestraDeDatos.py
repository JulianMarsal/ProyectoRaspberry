import time
import RPi.GPIO as GPIO
from temperatura import datos_sensor
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
from luma.core.legacy import text, show_message
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop

# Conexión de los sensores en sus respectivos pines
# Matriz --> vcc: 2, gnd: 6, din: 19, cs: 24, clk: 23
# Sonido --> a0: 7, gnd: 9, vc: 3, d0: 15
# Temperatura --> vcc: 1, sda: 11, clk: 14

# Activamos los sensores que vamos a usar
# matriz = Matriz(numero_matrices=2, ancho=16)

def config_matriz(cant_matrices=2, orientacion=0, rotacion=0, ancho=16, alto=8):   #Al ser 2 matrices se configura directamente un ancho de 16 para que imprima en las 2 juntas como una
        font = [CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT]
        serial = spi(port=0, device=0, gpio=noop())
        device = max7219(serial, width=ancho, height=alto, cascaded=cant_matrices, rotate=rotacion)
        return font,device

def config_sonido(canal=22):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(canal, GPIO.IN)
        # Desactivo las warnings por tener más de un circuito en la GPIO
        GPIO.setwarnings(False)
        GPIO.add_event_detect(canal, GPIO.RISING)
        return canal
	
def tomardatos():
    print ("Sonido detectado")
    dic_datos = datos_sensor()
    cadena_datos = 'Temperatura = {0:0.1f}°C  Humedad = {1:0.1f}%'.format(dic_datos["temp"], dic_datos["humedad"])
    return cadena_datos
    
    
def mostrar(mensaje, device, font, num_font=2,delay=0.1):
	show_message(device, mensaje, fill="white", font=proportional(font[num_font]), scroll_delay=delay)
	

def main():
	canal= config_sonido()
	font, device= config_matriz()
	while True:
		time.sleep(0.1)
		if GPIO.event_detected(canal):
			cadena=tomardatos()
			mostrar(cadena, device,font)
	GPIO.cleanup()
        
if __name__ == "__main__":
	main()  
