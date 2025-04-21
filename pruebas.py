from gpiozero import PWMLED
from time import sleep
import itertools

# Pines BCM de los LEDs (ajusta si necesitas)
led_red = PWMLED(17)
led_green = PWMLED(27)
led_blue = PWMLED(22)

# Mezcla de colores básicos (0.0 = apagado, 1.0 = encendido)
colores = [
    (1, 0, 0),    # Rojo
    (0, 1, 0),    # Verde
    (0, 0, 1),    # Azul
    (1, 1, 0),    # Amarillo
    (1, 0, 1),    # Magenta
    (0, 1, 1),    # Cian
    (1, 1, 1),    # Blanco
    (0.2, 0.5, 1),# Azul claro
    (0.9, 0.3, 0.7),  # Rosa fuerte
    (0.5, 0.2, 0.8),  # Violeta
    (0.5, 0.5, 0.5),  # Gris
    (1, 0.5, 0),      # Naranja
    (0.5, 1, 0),      # Verde claro
    (0.5, 0.5, 0),    # Amarillo claro
    (0.2, 0.2, 0.2),  # Gris oscuro
    (0.5, 0.5, 1),    # Azul oscuro
    (0.8, 0.8, 0),    # Amarillo fuerte
    (0.2, 0.8, 0.2),  # Verde fuerte
    (0.8, 0.2, 0.2),  # Rojo fuerte
    (1, 1, 1),        # Blanco brillante
    (0, 0, 0)     # Apagado
]

try:
    while True:
        for r, g, b in colores:
            led_red.value = r
            led_green.value = g
            led_blue.value = b
            sleep(1.5)

except KeyboardInterrupt:
    print("Interrumpido")

finally:
    led_red.value = 0
    led_green.value = 0
    led_blue.value = 0
