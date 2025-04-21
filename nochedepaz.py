from gpiozero import PWMLED, PWMOutputDevice
from time import sleep
import random

# Pines GPIO (ajusta si usás otros)
led_red = PWMLED(17)
led_green = PWMLED(27)
led_blue = PWMLED(22)
buzzer = PWMOutputDevice(12)

# Frecuencias de notas (Hz)
notes = {
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
    'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
    'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46, 'G5': 783.99,
    'R': 0  # Silencio
}

# 🎵 Duraciones musicales según figura (relativas al pulso)
BPM = 72
BEAT = 60 / BPM  # duración de una negra

# Mapear símbolos musicales a duraciones (en beats)
dur = {
    'w': 4.0,    # redonda
    'h': 2.0,    # blanca
    'hd': 3.0,   # blanca con puntillo
    'q': 1.0,    # negra
    'qd': 1.5,   # negra con puntillo
    'e': 0.5,    # corchea
    'ed': 0.75   # corchea con puntillo
}

# 🎶 Melodía completa de "Noche de Paz" con ritmo fiel y silencios
melody = [
    ('G4', 'q'), ('A4', 'q'), ('G4', 'e'), ('R', 'e'), ('E4', 'hd'),
    ('G4', 'q'), ('A4', 'q'), ('G4', 'e'), ('R', 'e'), ('E4', 'hd'),

    ('D5', 'q'), ('D5', 'q'), ('B4', 'e'), ('R', 'e'), ('C5', 'h'),
    ('A4', 'q'), ('G4', 'q'), ('E4', 'h'),

    ('G4', 'q'), ('G4', 'q'), ('C5', 'q'),
    ('B4', 'q'), ('A4', 'q'), ('G4', 'q'),
    ('A4', 'q'), ('G4', 'e'), ('R', 'e'), ('E4', 'hd'),

    ('D5', 'q'), ('D5', 'q'), ('F5', 'e'), ('R', 'e'), ('E5', 'h'),
    ('C5', 'q'), ('B4', 'q'), ('G4', 'hd'),

    ('A4', 'q'), ('A4', 'q'), ('C5', 'q'),
    ('B4', 'q'), ('A4', 'q'), ('G4', 'q'),
    ('A4', 'q'), ('G4', 'e'), ('R', 'e'), ('E4', 'hd'),

    ('D5', 'q'), ('D5', 'q'), ('F5', 'e'), ('R', 'e'), ('E5', 'h'),
    ('C5', 'q'), ('B4', 'q'), ('G4', 'hd')
]

REPETICIONES = 1

def set_color(r, g, b):
    led_red.value = r
    led_green.value = g
    led_blue.value = b

def play_note(note, figure):
    duration = dur[figure] * BEAT
    freq = notes[note]

    if freq == 0:
        buzzer.off()
        set_color(0, 0, 0)
        sleep(duration)
        return

    buzzer.frequency = freq
    buzzer.value = 0.5

    # Color aleatorio suave
    set_color(
        random.uniform(0.4, 1.0),
        random.uniform(0.4, 1.0),
        random.uniform(0.4, 1.0)
    )

    sleep(duration)
    buzzer.off()
    set_color(0, 0, 0)
    sleep(0.05)

try:
    for _ in range(REPETICIONES):
        for note, figure in melody:
            play_note(note, figure)
except KeyboardInterrupt:
    print("Interrumpido por el usuario.")
finally:
    buzzer.off()
    set_color(0, 0, 0)
