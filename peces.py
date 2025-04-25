from gpiozero import PWMLED, PWMOutputDevice
from time import sleep
import itertools
import board
import digitalio
import adafruit_character_lcd.character_lcd as character_lcd

# Pines del LCD
lcd_rs = digitalio.DigitalInOut(board.D26)
lcd_en = digitalio.DigitalInOut(board.D19)
lcd_d4 = digitalio.DigitalInOut(board.D13)
lcd_d5 = digitalio.DigitalInOut(board.D6)
lcd_d6 = digitalio.DigitalInOut(board.D5)
lcd_d7 = digitalio.DigitalInOut(board.D11)

lcd_columns = 16
lcd_rows = 2

lcd = character_lcd.Character_LCD_Mono(
    lcd_rs, lcd_en,
    lcd_d4, lcd_d5, lcd_d6, lcd_d7,
    lcd_columns, lcd_rows
)

# 👇 Definir la letra "ñ" como caracter personalizado (5x8)
custom_ñ = [
    0b00100,
    0b01010,
    0b00001,
    0b01111,
    0b10001,
    0b10001,
    0b10001,
    0b00000
]
lcd.create_char(0, custom_ñ)  # guardar en posición 0


# Pines GPIO
led_red = PWMLED(17)
led_green = PWMLED(27)
led_blue = PWMLED(22)
buzzer = PWMOutputDevice(12)

# Notas y silencios
notas_ingles = {
    'C3': 130.81, 'C#3': 138.59, 'D3': 146.83, 'D#3': 155.56, 'E3': 164.81,
    'F3': 174.61, 'F#3': 185.0, 'G3': 196.0, 'G#3': 207.65, 'A3': 220.0,
    'A#3': 233.08, 'B3': 246.94, 'C4': 261.63, 'C#4': 277.18, 'D4': 293.66,
    'D#4': 311.13, 'E4': 329.63, 'F4': 349.23, 'F#4': 369.99, 'G4': 392.0,
    'G#4': 415.3, 'A4': 440.0, 'A#4': 466.16, 'B4': 493.88, 'C5': 523.25,
    'C#5': 554.37, 'D5': 587.33, 'D#5': 622.25, 'E5': 659.26, 'F5': 698.46,
    'F#5': 739.99, 'G5': 783.99, 'G#5': 830.61, 'A5': 880.0, 'A#5': 932.33,
    'B5': 987.77, 'C6': 1046.5, 'C#6': 1108.73, 'D6': 1174.66, 'D#6': 1244.51,
    'E6': 1318.51, 'F6': 1396.91, 'F#6': 1479.98, 'G6': 1567.98, 'G#6': 1661.22,
    'A6': 1760.0, 'A#6': 1864.66, 'B6': 1975.53, 'C7': 2093.0, 'C#7': 2217.46,
    'D7': 2349.32, 'D#7': 2489.02, 'E7': 2637.02, 'F7': 2793.83, 'F#7': 2959.96,
    'G7': 3135.96, 'G#7': 3322.44, 'A7': 3520.0, 'A#7': 3729.31, 'B7': 3951.07,
    'C8': 4186.01, 'C#8': 4434.92, 'D8': 4698.64, 'D#8': 4978.03, 'R': 0
}

notas_latinas = {
    'Do3': 130.81, 'Do#3': 138.59, 'Re3': 146.83, 'Re#3': 155.56, 'Mi3': 164.81,
    'Fa3': 174.61, 'Fa#3': 185.0, 'Sol3': 196.0, 'Sol#3': 207.65, 'La3': 220.0,
    'La#3': 233.08, 'Si3': 246.94, 'Do4': 261.63, 'Do#4': 277.18, 'Re4': 293.66,
    'Re#4': 311.13, 'Mi4': 329.63, 'Fa4': 349.23, 'Fa#4': 369.99, 'Sol4': 392.0,
    'Sol#4': 415.3, 'La4': 440.0, 'La#4': 466.16, 'Si4': 493.88, 'Do5': 523.25,
    'Do#5': 554.37, 'Re5': 587.33, 'Re#5': 622.25, 'Mi5': 659.26, 'Fa5': 698.46,
    'Fa#5': 739.99, 'Sol5': 783.99, 'Sol#5': 830.61, 'La5': 880.0, 'La#5': 932.33,
    'Si5': 987.77, 'Do6': 1046.5, 'Do#6': 1108.73, 'Re6': 1174.66, 'Re#6': 1244.51,
    'Mi6': 1318.51, 'Fa6': 1396.91, 'Fa#6': 1479.98, 'Sol6': 1567.98, 'Sol#6': 1661.22,
    'La6': 1760.0, 'La#6': 1864.66, 'Si6': 1975.53, 'Do7': 2093.0, 'Do#7': 2217.46,
    'Re7': 2349.32, 'Re#7': 2489.02, 'Mi7': 2637.02, 'Fa7': 2793.83, 'Fa#7': 2959.96,
    'Sol7': 3135.96, 'Sol#7': 3322.44, 'La7': 3520.0, 'La#7': 3729.31, 'Si7': 3951.07,
    'Do8': 4186.01, 'Do#8': 4434.92, 'Re8': 4698.64, 'Re#8': 4978.03, 'R': 0
}

# Duración de figuras
BPM = 220
BEAT = 110 / BPM

dur = {
    'w': 4.0,
    'h': 2.0,
    'hd': 3.0,
    'q': 1.0,
    'qd': 1.5,
    'e': 0.5,
    'ed': 0.75,
    'he': 0.25,
}

# 🎵 Melodía completa CON silencios
melody = [
    ('R', 'q', ''), ('R', 'e', ''), ('La5', 'he', 'Pe'), ('Si5', 'he', 'ro'),
    ('Do6', 'e', 'Mi'), ('Do6', 'e', 'ra'), ('Do6', 'e', 'co'), ('Do6', 'e', 'mo'),
    ('Do6', 'q', 'be'), ('Si5', 'e', 'ben'), ('Do6', 'e', 'los'),
    ('Re6', 'e', 'pe'), ('Do6', 'e', 'ces'), ('Re6', 'e', 'en'), ('Do6', 'e', 'el'),
    ('Si5', 'e', 'ri'), ('Si5', 'e', 'o'), ('R', 'he', ''), ('Si5', 'he', 'pe'), ('Do6', 'he', 'ro'),
    ('Re6', 'e', 'mi'), ('Do6', 'e', 'ra'), ('Re6', 'e', 'co'), ('Do6', 'e', 'mo'),
    ('Si5', 'q', 'be'), ('Si5', 'e', 'ben'), ('Sol#5', 'e', 'por'), 
    ('La5', 'e', 'ver'), ('Si5', 'e', 'al'), ('Do6', 'e', 'dios'), ('Si5', 'e', 'na'),
    ('La5', 'e', 'ci'), ('La5', 'qd', 'do'),
    ('Do6', 'q', 'be'), ('Do6', 'e', 'ben'), ('Do6', 'e', 'y'),
    ('Do6', 'q', 'be'), ('Do6', 'e', 'ben'), ('Do6', 'e', 'y'),
    ('Re6', 'e', 'vuel'), ('Do6', 'e', 'ben'), ('Re6', 'e', 'a'), ('Do6', 'e', 'be'),
    ('Do', 'q', 'ver'), ('Re4', 'q', 'a'), ('Mi4', 'q', 'Dios'),
    ('Fa4', 'q', 'na'), ('Sol4', 'q', 'cer'), ('La4', 'h', ''),
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

def play_note(note, figure, lyric):
    duration = dur[figure] * BEAT
    freq = notas_latinas[note]

    # Mostrar la información en el LCD
    lcd.clear()
    lcd.message = f"{note},({figure} - {duration:.2f}s)\n{lyric}"


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
    for note, figure, lyric in melody:
        play_note(note, figure, lyric)
except KeyboardInterrupt:
    #print("Interrumpido.")
    lcd.clear()
    lcd.message = "Interrumpido."
    lcd.clear()
finally:
    buzzer.off()
    set_color(0, 0, 0)
    lcd.message = "Peces en el Rio \ncompleto con pausas"
    sleep(3)
    lcd.clear()
    lcd.message = "Peces en el Rio \ncompleto."
    sleep(3)
    lcd.clear()
