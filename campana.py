from gpiozero import PWMLED, PWMOutputDevice
from time import sleep
import random

# GPIO setup
led_red = PWMLED(17)
led_green = PWMLED(27)
led_blue = PWMLED(22)
buzzer = PWMOutputDevice(12)

# Notas (Hz)
notes = {
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
    'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
    'C5': 523.25, 'D5': 587.33, 'E5': 659.25,
    'R': 0
}

# Duraciones musicales
BPM = 88
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

# Funciones
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

    set_color(
        random.uniform(0.4, 1.0),
        random.uniform(0.4, 1.0),
        random.uniform(0.4, 1.0)
    )

    sleep(duration)
    buzzer.off()
    set_color(0, 0, 0)
    sleep(0.05)

# 🎵 Melodía común (intro)
estrofa_base = [
    ('E4', 'q'), ('F4', 'q'), ('G4', 'q'),
    ('E4', 'q'), ('F4', 'q'), ('G4', 'q'),
    ('A4', 'q'), ('G4', 'q'), ('F4', 'q'),
    ('E4', 'h'), ('R', 'q'),

    ('E4', 'q'), ('F4', 'q'), ('G4', 'q'),
    ('E4', 'q'), ('F4', 'q'), ('G4', 'q'),
    ('A4', 'q'), ('G4', 'q'), ('F4', 'q'),
    ('E4', 'h'), ('R', 'q'),

    ('G4', 'q'), ('G4', 'q'), ('A4', 'q'),
    ('G4', 'q'), ('F4', 'q'), ('E4', 'q'),
    ('F4', 'q'), ('F4', 'q'), ('G4', 'q'),
    ('F4', 'h'), ('R', 'q')
]

# Final estrofa 1 (verás al Niño en la cuna)
final_1 = [
    ('G4', 'q'), ('G4', 'q'), ('A4', 'q'),
    ('G4', 'q'), ('F4', 'q'), ('E4', 'q'),
    ('D4', 'q'), ('C4', 'q'), ('D4', 'q'),
    ('C4', 'hd'), ('R', 'q')
]

# Final estrofa 2 (agua de la madrugada)
final_2 = [
    ('G4', 'q'), ('F4', 'q'), ('G4', 'q'),
    ('A4', 'q'), ('A4', 'q'), ('G4', 'q'),
    ('F4', 'q'), ('E4', 'q'), ('D4', 'q'),
    ('C4', 'hd'), ('R', 'q')
]

# Final estrofa 3 (me voy a Belén)
final_3 = [
    ('E4', 'q'), ('F4', 'q'), ('G4', 'q'),
    ('A4', 'q'), ('G4', 'q'), ('E4', 'q'),
    ('F4', 'q'), ('D4', 'q'), ('C4', 'q'),
    ('C4', 'hd'), ('R', 'q')
]

# 🎶 Juntar todo
melody = (
    estrofa_base + final_1 + [('R', 'w')] +
    estrofa_base + final_2 + [('R', 'w')] +
    estrofa_base + final_3
)

# ▶️ Reproducir
try:
    for note, figure in melody:
        play_note(note, figure)
except KeyboardInterrupt:
    print("Interrumpido.")
finally:
    buzzer.off()
    set_color(0, 0, 0)
