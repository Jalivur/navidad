from gpiozero import PWMLED, PWMOutputDevice
from time import sleep
import itertools
import random
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
BPM = 690
BEAT = 160 / BPM

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
    # 'Entrada 
    ('Sol6', 'e', ''), ('Mi6', 'e', ''), ('Do6', 'e', ''), ('Sol6', 'e', ''),
    ('Mi6', 'e', ''), ('Do6', 'e', ''), ('Sol6', 'e', ''), ('Mi5', 'e', ''),
    ('Re6', 'q', ''), ('Si5', 'e', ''), ('Sol5', 'e', ''),
    ('R', 'e', ''), ('Sol5', 'e', ''), ('Si5', 'e', ''), ('Re6', 'e', ''),
    ('Do6', 'q', ''), ('La5', 'e', ''), ('Fa#5', 'e', ''),
    ('R', 'e', ''), ('Do6', 'e', ''), ('Si5', 'e', ''), ('La5', 'e', ''),
    ('Si5', 'q', ''), ('Do6', 'e', ''), ('Re6', 'h', ''),
    ('Sol6', 'e', ''), ('Mi6', 'e', ''), ('Do6', 'e', ''), ('Sol6', 'e', ''),
    ('Mi6', 'e', ''), ('Do6', 'e', ''), ('Sol6', 'e', ''), ('Mi5', 'e', ''),
    ('Re6', 'q', ''), ('Si5', 'e', ''), ('Sol5', 'e', ''),
    ('R', 'e', ''), ('Sol5', 'e', ''), ('Si5', 'e', ''), ('Re6', 'e', ''),
    ('Do6', 'q', ''), ('La5', 'e', ''), ('Fa#5', 'e', ''),
    ('R', 'e', ''), ('Do6', 'e', ''), ('Si5', 'e', ''), ('La5', 'e', ''),
    ('Sol5', 'q', ''), ('R', 'e', ''), ('Sol5', 'e', 'con'), ('Sol5', 'q', 'mi'), ('Sol5', 'q', 'bu'),
    # 'Estrofa 1'
    ('Sol5', 'q', 'rri'), ('Sol5', 'q', 'to'), ('Sol5', 'q', 'sa'), ('Sol5', 'q', 'ba'),
    ('Do6', 'qd', 'ne'), ('Do6', 'e', 'ro'), ('Do6', 'q', 'voy'), ('Do6', 'q', 'ca'), 
    ('La5', 'q', 'mi'), ('La5', 'q', 'no'), ('Sol5', 'q', 'de'), ('La5', 'q', 'be'),
    ('Si5', 'e', 'len'), ('Sol5', 'q', '__'), ('Sol5', 'e', 'con'), ('Sol5', 'q', 'mi'), ('Sol5', 'q', 'bu'),
    ('Sol5', 'q', 'rri'), ('Sol5', 'q', 'to'), ('Sol5', 'q', 'sa'), ('Sol5', 'q', 'ba'),
    ('Do6', 'qd', 'ne'), ('Do6', 'e', 'ro'), ('Do6', 'q', 'voy'), ('Do6', 'q', 'ca'), 
    ('La5', 'q', 'mi'), ('La5', 'q', 'no'), ('Sol5', 'q', 'de'), ('La5', 'q', 'be'),
    ('Si5', 'e', 'len'), ('Sol5', 'qd', '__'), 
    ('Sol5', 'q', 'si'), ('Sol5', 'q', 'me'), ('Sol5', 'h', 'ven'), 
    ('Sol5', 'q', 'si'), ('Sol5', 'q', 'me'), ('Sol5', 'h', 'ven'),
    ('Si5', 'q', 'voy'), ('Si5', 'q', 'ca'), ('La5', 'q', 'mi'), ('La5', 'q', 'no'),
    ('Sol5', 'q', 'de'), ('Fa#5', 'q', 'be'), ('Sol5', 'h', 'len'),
    ('Sol5', 'q', 'si'), ('Sol5', 'q', 'me'),('Sol5', 'h', 'ven'), 
    ('Sol5', 'q', 'si'), ('Sol5', 'q', 'me'), ('Sol5', 'h', 'ven'),
    ('Si5', 'q', 'voy'), ('Si5', 'q', 'ca'), ('La5', 'q', 'mi'), ('La5', 'q', 'no'),
    ('Sol5', 'q', 'de'), ('Fa#5', 'q', 'be'), ('Sol5', 'qd', 'len'),
    ('Sol5', 'e', 'el'), ('Sol5', 'q', 'lu'), ('Sol5', 'q', 'ce'),
    # 'Estrofa 2'
    ('Sol5', 'q', 'ri'), ('Sol5', 'q', 'to'), ('Sol5', 'q', 'ma'), ('Sol5', 'q', '\x00a'),
    ('Do6', 'qd', 'ne'), ('Do6', 'e', 'ro'), ('Do6', 'q', 'ilu'), ('Do6', 'q', 'mi'), 
    ('La5', 'q', 'na'), ('La5', 'q', 'mi'), ('Sol5', 'q', 'sen'), ('La5', 'q', 'de'),
    ('Si5', 'e', 'ro'), ('Sol5', 'q', '__'), ('Sol5', 'e', 'el'), ('Sol5', 'q', 'lu'), ('Sol5', 'q', 'ce'),
    ('Sol5', 'q', 'ri'), ('Sol5', 'q', 'to'), ('Sol5', 'q', 'ma'), ('Sol5', 'q', '\x00a'),
    ('Do6', 'qd', 'ne'), ('Do6', 'e', 'ro'), ('Do6', 'q', 'ily'), ('Do6', 'q', 'mi'), 
    ('La5', 'q', 'na'), ('La5', 'q', 'mi'), ('Sol5', 'q', 'sen'), ('La5', 'q', 'de'),
    ('Si5', 'e', 'ro'), ('Sol5', 'qd', '__'), 
    ('Sol5', 'q', 'si'), ('Sol5', 'q', 'me'), ('Sol5', 'h', 'ven'), 
    ('Sol5', 'q', 'si'), ('Sol5', 'q', 'me'), ('Sol5', 'h', 'ven'),
    ('Si5', 'q', 'voy'), ('Si5', 'q', 'ca'), ('La5', 'q', 'mi'), ('La5', 'q', 'no'),
    ('Sol5', 'q', 'de'), ('Fa#5', 'q', 'be'), ('Sol5', 'h', 'len'),
    ('Sol5', 'q', 'si'), ('Sol5', 'q', 'me'),('Sol5', 'h', 'ven'), 
    ('Sol5', 'q', 'si'), ('Sol5', 'q', 'me'), ('Sol5', 'h', 'ven'),
    ('Si5', 'q', 'voy'), ('Si5', 'q', 'ca'), ('La5', 'q', 'mi'), ('La5', 'q', 'no'),
    ('Sol5', 'q', 'de'), ('Fa#5', 'q', 'be'), ('Sol5', 'w', 'len'),

    
    # 'Estribillo'
    ('Si5', 'ed', 'Tu'), ('Si5', 'e', 'qui'), ('Si5', 'ed', 'Tu'), ('Si5', 'e', 'qui'),
    ('Si5', 'e', 'Tu'), ('Si5', 'e', 'Qui'),('Sol5', 'q', 'Tu'), ('Mi5', 'hd', 'qui'), 
    ('Si5', 'ed', 'Tu'), ('Si5', 'e', 'qui'), ('Si5', 'ed', 'Tu'), ('Si5', 'e', 'qui'),
    ('Si5', 'ed', 'Tu'), ('Si5', 'e', 'Qui'), 
    ('Sol5', 'w', 'Tu'),
    
    ('La5', 'e', 'A'), ('La5', 'e', 'pu'), ('La5', 'e', 'ra'), ('La5', 'e', 'te'),
    ('La5', 'q', 'mi'), ('Sol5', 'q', 'bu'),
    ('Fa#5', 'q', 'rri'), ('Re5', 'qd', 'to'),
    ('La5', 'e', 'que'), ('La5', 'e', 'ya'), ('La5', 'e', 'va'), ('La5', 'e', 'mos'),
    ('La5', 'q', 'a'), ('Sol5', 'q', 'lle'),
    ('Fa#5', 'w', 'gar'),
    
    ('Si5', 'ed', 'Tu'), ('Si5', 'ed', 'qui'), ('Si5', 'ed', 'tu'), ('Si5', 'e', 'qui'), 
    ('Si5', 'ed', 'tu'), ('La5', 'e', 'qui'),
    ('Sol5', 'q', 'tu'), ('Mi5', 'hd', 'qui'),
    
    ('Si5', 'ed', 'tu'), ('Si5', 'e', '_'), ('Si5', 'ed', 'qui'), ('Si5', 'e', 'tu'),
    ('Si5', 'ed', '_'), ('Si5', 'e', 'qui'),
    ('Sol5', 'h', 'tu'), ('Sol5', 'q', 'a'), ('Sol5', 'q', 'pu'),
    ('Sol5', 'q', 'ra'), ('Sol5', 'q', 'te'), ('Sol5', 'q', 'mi'), ('Sol5', 'q', 'bu'),
    ('Si5', 'q', 'rri'), ('Sol5', 'q', 'to'), ('Re5', 'q', 'va'), ('Si5', 'q', 'mos'),
    ('La5', 'q', 'a'), ('Sol5', 'q', 'ver'), ('Fa#5', 'q', 'a'), ('La5', 'q', 'Je'),
    ('Sol5', 'qd', 'sus'),
    ('Sol5', 'e', 'con'), ('Sol5', 'q', 'mi'), ('Sol5', 'q', 'bu'),
    
    # 'Estrofa 1'
    ('Sol5', 'q', 'rri'), ('Sol5', 'q', 'to'), ('Sol5', 'q', 'sa'), ('Sol5', 'q', 'ba'),
    ('Do6', 'qd', 'ne'), ('Do6', 'e', 'ro'), ('Do6', 'q', 'voy'), ('Do6', 'q', 'ca'), 
    ('La5', 'q', 'mi'), ('La5', 'q', 'no'), ('Sol5', 'q', 'de'), ('La5', 'q', 'be'),
    ('Si5', 'e', 'len'), ('Sol5', 'q', '__'), ('Sol5', 'e', 'con'), ('Sol5', 'q', 'mi'), ('Sol5', 'q', 'bu'),
    ('Sol5', 'q', 'rri'), ('Sol5', 'q', 'to'), ('Sol5', 'q', 'sa'), ('Sol5', 'q', 'ba'),
    ('Do6', 'qd', 'ne'), ('Do6', 'e', 'ro'), ('Do6', 'q', 'voy'), ('Do6', 'q', 'ca'), 
    ('La5', 'q', 'mi'), ('La5', 'q', 'no'), ('Sol5', 'q', 'de'), ('La5', 'q', 'be'),
    ('Si5', 'e', 'len'), ('Sol5', 'qd', '__'), 
    ('Sol5', 'q', 'si'), ('Sol5', 'q', 'me'), ('Sol5', 'h', 'ven'), 
    ('Sol5', 'q', 'si'), ('Sol5', 'q', 'me'), ('Sol5', 'h', 'ven'),
    ('Si5', 'q', 'voy'), ('Si5', 'q', 'ca'), ('La5', 'q', 'mi'), ('La5', 'q', 'no'),
    ('Sol5', 'q', 'de'), ('Fa#5', 'q', 'be'), ('Sol5', 'h', 'len'),
    ('Sol5', 'q', 'si'), ('Sol5', 'q', 'me'),('Sol5', 'h', 'ven'), 
    ('Sol5', 'q', 'si'), ('Sol5', 'q', 'me'), ('Sol5', 'h', 'ven'),
    ('Si5', 'q', 'voy'), ('Si5', 'q', 'ca'), ('La5', 'q', 'mi'), ('La5', 'q', 'no'),
    ('Sol5', 'q', 'de'), ('Fa#5', 'q', 'be'), ('Sol5', 'qd', 'len'),
    ('Sol5', 'e', 'el'), ('Sol5', 'q', 'lu'), ('Sol5', 'q', 'ce'),
    # 'Estrofa 2'
    ('Sol5', 'q', 'ri'), ('Sol5', 'q', 'to'), ('Sol5', 'q', 'ma'), ('Sol5', 'q', '\x00a'),
    ('Do6', 'qd', 'ne'), ('Do6', 'e', 'ro'), ('Do6', 'q', 'ilu'), ('Do6', 'q', 'mi'), 
    ('La5', 'q', 'na'), ('La5', 'q', 'mi'), ('Sol5', 'q', 'sen'), ('La5', 'q', 'de'),
    ('Si5', 'e', 'ro'), ('Sol5', 'q', '__'), ('Sol5', 'e', 'el'), ('Sol5', 'q', 'lu'), ('Sol5', 'q', 'ce'),
    ('Sol5', 'q', 'ri'), ('Sol5', 'q', 'to'), ('Sol5', 'q', 'ma'), ('Sol5', 'q', '\x00a'),
    ('Do6', 'qd', 'ne'), ('Do6', 'e', 'ro'), ('Do6', 'q', 'ily'), ('Do6', 'q', 'mi'), 
    ('La5', 'q', 'na'), ('La5', 'q', 'mi'), ('Sol5', 'q', 'sen'), ('La5', 'q', 'de'),
    ('Si5', 'e', 'ro'), ('Sol5', 'qd', '__'), 
    ('Sol5', 'q', 'si'), ('Sol5', 'q', 'me'), ('Sol5', 'h', 'ven'), 
    ('Sol5', 'q', 'si'), ('Sol5', 'q', 'me'), ('Sol5', 'h', 'ven'),
    ('Si5', 'q', 'voy'), ('Si5', 'q', 'ca'), ('La5', 'q', 'mi'), ('La5', 'q', 'no'),
    ('Sol5', 'q', 'de'), ('Fa#5', 'q', 'be'), ('Sol5', 'h', 'len'),
    ('Sol5', 'q', 'si'), ('Sol5', 'q', 'me'),('Sol5', 'h', 'ven'), 
    ('Sol5', 'q', 'si'), ('Sol5', 'q', 'me'), ('Sol5', 'h', 'ven'),
    ('Si5', 'q', 'voy'), ('Si5', 'q', 'ca'), ('La5', 'q', 'mi'), ('La5', 'q', 'no'),
    ('Sol5', 'q', 'de'), ('Fa#5', 'q', 'be'), ('Sol5', 'w', 'len'),
    
    # 'Estribillo'
    ('Si5', 'ed', 'Tu'), ('Si5', 'e', 'qui'), ('Si5', 'ed', 'Tu'), ('Si5', 'e', 'qui'),
    ('Si5', 'e', 'Tu'), ('Si5', 'e', 'Qui'),('Sol5', 'q', 'Tu'), ('Mi5', 'hd', 'qui'), 
    ('Si5', 'ed', 'Tu'), ('Si5', 'e', 'qui'), ('Si5', 'ed', 'Tu'), ('Si5', 'e', 'qui'),
    ('Si5', 'ed', 'Tu'), ('Si5', 'e', 'Qui'), 
    ('Sol5', 'w', 'Tu'),
    
    ('La5', 'e', 'A'), ('La5', 'e', 'pu'), ('La5', 'e', 'ra'), ('La5', 'e', 'te'),
    ('La5', 'q', 'mi'), ('Sol5', 'q', 'bu'),
    ('Fa#5', 'q', 'rri'), ('Re5', 'qd', 'to'),
    ('La5', 'e', 'que'), ('La5', 'e', 'ya'), ('La5', 'e', 'va'), ('La5', 'e', 'mos'),
    ('La5', 'q', 'a'), ('Sol5', 'q', 'lle'),
    ('Fa#5', 'w', 'gar'),
    
    ('Si5', 'ed', 'Tu'), ('Si5', 'ed', 'qui'), ('Si5', 'ed', 'tu'), ('Si5', 'e', 'qui'), 
    ('Si5', 'ed', 'tu'), ('La5', 'e', 'qui'),
    ('Sol5', 'q', 'tu'), ('Mi5', 'hd', 'qui'),
    
    ('Si5', 'ed', 'tu'), ('Si5', 'e', '_'), ('Si5', 'ed', 'qui'), ('Si5', 'e', 'tu'),
    ('Si5', 'ed', '_'), ('Si5', 'e', 'qui'),
    ('Sol5', 'h', 'tu'), ('Sol5', 'q', 'a'), ('Sol5', 'q', 'pu'),
    ('Sol5', 'q', 'ra'), ('Sol5', 'q', 'te'), ('Sol5', 'q', 'mi'), ('Sol5', 'q', 'bu'),
    ('Si5', 'q', 'rri'), ('Sol5', 'q', 'to'), ('Re5', 'q', 'va'), ('Si5', 'q', 'mos'),
    ('La5', 'q', 'a'), ('Sol5', 'q', 'ver'), ('Fa#5', 'q', 'a'), ('La5', 'q', 'Je'),
    ('Sol5', 'qd', 'sus'),
    ('Sol5', 'e', 'con'), ('Sol5', 'q', 'mi'), ('Sol5', 'q', 'bu'),
    
    # 'Estrofa 1'
    ('Sol5', 'q', 'rri'), ('Sol5', 'q', 'to'), ('Sol5', 'q', 'sa'), ('Sol5', 'q', 'ba'),
    ('Do6', 'qd', 'ne'), ('Do6', 'e', 'ro'), ('Do6', 'q', 'voy'), ('Do6', 'q', 'ca'), 
    ('La5', 'q', 'mi'), ('La5', 'q', 'no'), ('Sol5', 'q', 'de'), ('La5', 'q', 'be'),
    ('Si5', 'e', 'len'),
    ('Sol5', 'q', 'si'), ('Sol5', 'q', 'me'), ('Sol5', 'h', 'ven'), 
    ('Sol5', 'q', 'si'), ('Sol5', 'q', 'me'), ('Sol5', 'h', 'ven'),
    ('Si5', 'q', 'voy'), ('Si5', 'q', 'ca'), ('La5', 'q', 'mi'), ('La5', 'q', 'no'),
    ('Sol5', 'q', 'de'), ('Fa#5', 'q', 'be'), ('Sol5', 'h', 'len'),
    ('Sol5', 'q', 'si'), ('Sol5', 'q', 'me'), ('Sol5', 'h', 'ven'), 
    ('Sol5', 'q', 'si'), ('Sol5', 'q', 'me'), ('Sol5', 'h', 'ven'),
    ('Si5', 'q', 'voy'), ('Si5', 'q', 'ca'), ('La5', 'q', 'mi'), ('La5', 'q', 'no'),
    ('Sol5', 'q', 'de'), ('Fa#5', 'q', 'be'), ('Sol5', 'h', 'len'),
    ('R', 'q', ''), ('R', 'q', ''),
]

# Generar todas las combinaciones posibles de colores RGB
steps = [i / 10 for i in range(11)]  # Generar valores de 0.0 a 1.0 con incrementos de 0.1
color_sequence = list(itertools.product(steps, repeat=3))  # Generar combinaciones

# Mezclar la secuencia de colores de forma aleatoria
random.shuffle(color_sequence)

# Crear un ciclo infinito de colores
color_cycle = itertools.cycle(color_sequence)

# Función para establecer el color
def set_color(r, g, b):
    led_red.value = r
    led_green.value = g
    led_blue.value = b

# Función para reproducir una nota con un color
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
    r, g, b = next(color_cycle)  # Obtener el siguiente color aleatorio
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
    lcd.clear()
    lcd.message = "Burrito Sabanero \ncompleto."
    sleep(3)
    lcd.clear()
