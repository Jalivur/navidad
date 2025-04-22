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
    0b10000,
    0b1110,
    0b10001,
    0b10001,
    0b10001,
    0b00000
]
lcd.create_char(0, custom_ñ)  # guardar en posición 0
# 👇 Definir el caracter "¡" como caracter personalizado (5x8)
custom_ex = [
    0b00000,
    0b00100,
    0b00000,
    0b00000,
    0b00100,
    0b00100,
    0b00100,
    0b00100
]
lcd.create_char(1, custom_ex)  # guardar en posición 1

# LEDs y buzzer
led_red = PWMLED(17)
led_green = PWMLED(27)
led_blue = PWMLED(22)
buzzer = PWMOutputDevice(12)

# Notas con sus frecuencias
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

# Ritmos en negras, corcheas, etc.
BPM = 190
BEAT = 60 / BPM

dur = {
    'w': 4.0, 'h': 2.0, 'hd': 3.0,
    'q': 1.0, 'qd': 1.5, 'e': 0.5,
    'ed': 0.75, 's': 0.25
}

# 🎶 Cumpleaños Feliz con "ñ" personalizada (\x00)
melody = [
    ('Do4', 'q', 'Cum'), ('Do4', 'q', 'ple'), ('Re4', 'q', 'a'),
    ('Do4', 'qd', '\x00os'), ('Fa4', 'q', 'fe'), ('Mi4', 'h', 'liz'),

    ('Do4', 'q', 'Cum'), ('Do4', 'q', 'ple'), ('Re4', 'q', 'a'),
    ('Do4', 'qd', '\x00os'), ('Sol4', 'q', 'fe'), ('Fa4', 'h', 'liz'),

    ('Do4', 'q', 'Te'), ('Do4', 'q', 'De'), ('Do5', 'qd', 'se'), ('La4', 'q', 'a'), ('Fa4', 'q', 'mos'),
    ('Mi4', 'q', 'Pa'), ('Re4', 'h', 'blo'), ('La#4', 'q', 'cum'), ('La#4', 'q', 'ple'),

    ('La4', 'q', 'a'), ('Fa4', 'qd', '\x00os'), ('Sol4', 'q', 'fe'), ('Fa4', 'h', 'liz'),
    ('R', 'q', ''),  # silencio final
]

# Colores arcoíris para LEDs
color_sequence = [
    (1.0, 0.2, 0.2), (1.0, 1.0, 0.2), (0.2, 1.0, 0.4),
    (0.2, 0.8, 1.0), (0.5, 0.3, 1.0), (1.0, 0.5, 0.8),
    (0.8, 0.5, 1.0), (0.5, 1.0, 0.5), (1.0, 1.0, 1.0),
    (0.2, 0.2, 0.2), (0.5, 0.5, 0.5), (1.0, 0.5, 0)
]
color_cycle = itertools.cycle(color_sequence)

# Función para cambiar colores
def set_color(r, g, b):
    led_red.value = r
    led_green.value = g
    led_blue.value = b

# Función para reproducir cada nota
def play_note(note, figure, lyric):
    duration = dur[figure] * BEAT
    freq = notas_latinas[note]

    #print(f"{note} ({figure}) -> {lyric}")
    lcd.clear()
    lcd.message = f"{note} ({figure})\n {lyric}"

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

# 🎉 Reproducción principal
try:
    lcd.clear()
    lcd.message = "\x01Feliz cumplea\x00os\nPABLO!"
    sleep(3)
    lcd.clear()
    lcd.message = "Mama Y Papa\nTe quieren"
    sleep(3)
    lcd.clear()

    for note, figure, lyric in melody:
        play_note(note, figure, lyric)
    sleep(1)
    for note, figure, lyric in melody:
        play_note(note, figure, lyric)

except KeyboardInterrupt:
    #print("Interrumpido.")
    lcd.message = "Interrumpido."
    sleep(1)
    lcd.clear()

finally:
    buzzer.off()
    set_color(0, 0, 0)
    lcd.message = "\x01Felicidades\nPablo!"
    sleep(3)
    lcd.clear()
    lcd.message = "\x01Mama Y Papa\nTe quieren!"
    sleep(3)
    lcd.clear() 
