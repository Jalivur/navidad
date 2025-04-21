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
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23, 'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
    'C5': 523.25, 'R': 0  # R es silencio
}

# Melodía de "Estrellita del lugar"
melody = [
    ('C4', 0.5), ('C4', 0.5), ('G4', 0.5), ('G4', 0.5), 
    ('A4', 0.5), ('A4', 0.5), ('G4', 1.0),  # Primera línea

    ('F4', 0.5), ('F4', 0.5), ('E4', 0.5), ('E4', 0.5), 
    ('D4', 0.5), ('D4', 0.5), ('C4', 1.0),  # Segunda línea

    ('G4', 0.5), ('G4', 0.5), ('F4', 0.5), ('F4', 0.5),
    ('E4', 0.5), ('E4', 0.5), ('D4', 1.0),  # Tercera línea

    ('C4', 0.5), ('C4', 0.5), ('G4', 0.5), ('G4', 0.5), 
    ('A4', 0.5), ('A4', 0.5), ('G4', 1.0),  # Cuarta línea
]

# Repeticiones de la canción
REPETICIONES = 2

def set_color(r, g, b):
    led_red.value = r
    led_green.value = g
    led_blue.value = b

def play_note(note, duration):
    freq = notes[note]
    if freq == 0:  # Si la nota es silencio
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
