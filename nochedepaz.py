from gpiozero import PWMLED, PWMOutputDevice
from time import sleep
import random
import colorsys

# Pines GPIO
led_red = PWMLED(17)
led_green = PWMLED(27)
led_blue = PWMLED(22)
buzzer = PWMOutputDevice(12)

# Notas musicales (frecuencias en Hz)
notes = {
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
    'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
    'C5': 523.25, 'D5': 587.33, 'E5': 659.25,
    'F5': 698.46, 'G5': 783.99,
    'R': 0  # Silencio
}

# Duraciones musicales en relación al beat
BPM = 90
BEAT = 60 / BPM  # Una negra

dur = {
    'w': 4.0,
    'h': 2.0,
    'hd': 3.0,
    'q': 1.0,
    'qd': 1.5,
    'e': 0.5,
    'ed': 0.75
}

# Melodía fiel de “Noche de Paz” según partitura
melody = [
    ('G4', 'q'), ('G4', 'q'), ('A4', 'q'), ('G4', 'q'), ('E4', 'h'),
    ('G4', 'q'), ('G4', 'q'), ('A4', 'q'), ('G4', 'q'), ('E4', 'h'),

    ('D5', 'q'), ('D5', 'q'), ('B4', 'q'), ('C5', 'q'), ('A4', 'q'), ('G4', 'q'), ('E4', 'h'),

    ('G4', 'q'), ('G4', 'q'), ('C5', 'q'),
    ('B4', 'q'), ('A4', 'q'), ('G4', 'q'),
    ('A4', 'q'), ('G4', 'e'), ('R', 'e'), ('E4', 'h'),

    ('D5', 'q'), ('D5', 'q'), ('F5', 'e'), ('R', 'e'), ('E5', 'q'),
    ('C5', 'q'), ('B4', 'q'), ('G4', 'hd'),

    ('A4', 'q'), ('A4', 'q'), ('C5', 'q'),
    ('B4', 'q'), ('A4', 'q'), ('G4', 'q'),
    ('A4', 'q'), ('G4', 'e'), ('R', 'e'), ('E4', 'hd'),

    ('D5', 'q'), ('D5', 'q'), ('F5', 'e'), ('R', 'e'), ('E5', 'q'),
    ('C5', 'q'), ('B4', 'q'), ('G4', 'hd')
]

# Número de repeticiones de la canción
REPETICIONES = 2

# Función para mezclar colores tipo arcoíris
def rainbow_color():
    hue = random.random()
    r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
    return r, g, b

# Establece el color RGB en los LEDs
def set_color(r, g, b):
    led_red.value = r
    led_green.value = g
    led_blue.value = b

# Reproduce una nota con duración y LEDs
def play_note(note, figure):
    duration = dur[figure] * BEAT
    freq = notes[note]

    print(f"Tocando: {note} ({figure}) - {duration:.2f}s")

    if freq == 0:
        buzzer.off()
        set_color(0, 0, 0)
        sleep(duration)
        return

    buzzer.frequency = freq
    buzzer.value = 0.5

    # Cambiar color en cada nota (arcoíris)
    r, g, b = rainbow_color()
    set_color(r, g, b)

    sleep(duration)
    buzzer.off()
    set_color(0, 0, 0)
    sleep(0.05)

# Reproducción principal
try:
    for _ in range(REPETICIONES):
        for note, figure in melody:
            play_note(note, figure)

except KeyboardInterrupt:
    print("\nInterrumpido por el usuario.")

finally:
    buzzer.off()
    set_color(0, 0, 0)
    print("GPIO liberado. ¡Feliz Navidad! 🎄")
