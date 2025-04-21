from gpiozero import PWMLED, PWMOutputDevice
from time import sleep
import random

# Pines BCM
led_red = PWMLED(17)
led_green = PWMLED(27)
led_blue = PWMLED(22)
buzzer = PWMOutputDevice(12)

# Notas musicales (frecuencias aproximadas)
notes = {
    'B4': 494, 'A4': 440, 'G4': 392, 'E4': 330, 'D4': 294, 'C4': 262,
    'F4': 349, 'G5': 784, 'E5': 659, 'D5': 587, 'C5': 523, 'A5': 880, 'R': 0
}

# Melodía simplificada
melody = [
    ('E4', 0.5), ('E4', 0.5), ('E4', 1.0),
    ('E4', 0.5), ('E4', 0.5), ('E4', 1.0),
    ('E4', 0.5), ('G4', 0.5), ('C4', 0.5), ('D4', 0.5),
    ('E4', 1.5),
]

# Repeticiones de la canción
REPETICIONES = 2

def set_color(r, g, b):
    led_red.value = r
    led_green.value = g
    led_blue.value = b

def play_note(note, duration):
    freq = notes[note]
    if freq == 0:
        set_color(0, 0, 0)
        sleep(duration)
        return

    # Establecer frecuencia en el buzzer
    buzzer.frequency = freq  # Establecer la frecuencia del buzzer
    
    # Generar el tono
    buzzer.value = 0.5  # Establecer ciclo de trabajo al 50% para generar el tono

    # Cambiar color de los LEDs
    r = random.uniform(0.3, 1.0)
    g = random.uniform(0.3, 1.0)
    b = random.uniform(0.3, 1.0)
    set_color(r, g, b)

    # Reproducir el tono por la duración de la nota
    sleep(duration)
    buzzer.off()  # Apagar el buzzer
    set_color(0, 0, 0)  # Apagar los LEDs
    sleep(0.05)  # Pausa entre notas

try:
    for _ in range(REPETICIONES):
        for note, duration in melody:
            play_note(note, duration)

except KeyboardInterrupt:
    print("Interrumpido por el usuario")
finally:
    set_color(0, 0, 0)
    buzzer.off()
