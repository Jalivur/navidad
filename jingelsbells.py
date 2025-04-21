from gpiozero import PWMLED, PWMOutputDevice
from time import sleep
import itertools

# Pines GPIO
led_red = PWMLED(17)
led_green = PWMLED(27)
led_blue = PWMLED(22)
buzzer = PWMOutputDevice(12)

# Notas y silencios
notes = {
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
    'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
    'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46,
    'G5': 783.99, 'R': 0
}

# Duración de figuras
BPM = 180
BEAT = 60 / BPM

dur = {
    'w': 4.0,
    'h': 2.0,
    'hd': 3.0,
    'q': 1.0,
    'qd': 1.5,
    'e': 0.5,
    'ed': 0.75
}

# 🎵 Melodía completa CON silencios
melody = [
    # --- Estrofa ---
    ('E4', 'q'), ('E4', 'q'), ('E4', 'h'),
    ('E4', 'q'), ('E4', 'q'), ('E4', 'h'),
    ('E4', 'q'), ('G4', 'q'), ('C4', 'q'), ('D4', 'q'),
    ('E4', 'w'), ('R', 'q'),

    ('F4', 'q'), ('F4', 'q'), ('F4', 'ed'), ('F4', 'e'),
    ('F4', 'q'), ('E4', 'q'), ('E4', 'q'), ('E4', 'e'), ('E4', 'e'),
    ('E4', 'q'), ('D4', 'q'), ('D4', 'q'), ('E4', 'q'),
    ('D4', 'h'), ('G4', 'h'), ('R', 'h'),

    # --- Estribillo ---
    ('E4', 'q'), ('E4', 'q'), ('E4', 'q'), ('E4', 'q'),
    ('E4', 'q'), ('E4', 'q'), ('E4', 'q'), ('G4', 'q'),
    ('C4', 'q'), ('D4', 'q'), ('E4', 'h'), ('R', 'q'),

    ('F4', 'q'), ('F4', 'q'), ('F4', 'q'), ('F4', 'q'),
    ('F4', 'q'), ('E4', 'q'), ('E4', 'q'), ('E4', 'q'), ('E4', 'q'),
    ('D4', 'q'), ('D4', 'q'), ('E4', 'q'),
    ('D4', 'h'), ('G4', 'h'), ('R', 'w')
]

# Colores rotativos
color_sequence = [
    (1.0, 0.2, 0.2), (1.0, 1.0, 0.2), (0.2, 1.0, 0.4),
    (0.2, 0.8, 1.0), (0.5, 0.3, 1.0), (1.0, 0.5, 0.8),
    (0.8, 0.5, 1.0), (0.5, 1.0, 0.5), (1.0, 1.0, 1.0),
    (0.2, 0.2, 0.2), (0.5, 0.5, 0.5), (1.0, 0.5, 0)
]
color_cycle = itertools.cycle(color_sequence)

# Funciones
def set_color(r, g, b):
    led_red.value = r
    led_green.value = g
    led_blue.value = b

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
    r, g, b = next(color_cycle)
    set_color(r, g, b)

    sleep(duration)
    buzzer.off()
    set_color(0, 0, 0)
    sleep(0.05)

# Reproducción principal
try:
    for note, figure in melody:
        play_note(note, figure)
except KeyboardInterrupt:
    print("Interrumpido.")
finally:
    buzzer.off()
    set_color(0, 0, 0)
    print("¡Jingle Bells completo con pausas! 🎄🎶")
