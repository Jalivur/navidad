from gpiozero import PWMLED, PWMOutputDevice
from time import sleep
import random
import colorsys
import itertools
import board
import digitalio
import adafruit_character_lcd.character_lcd as character_lcd
import threading

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


# Pines GPIO
led_red = PWMLED(17)
led_green = PWMLED(27)
led_blue = PWMLED(22)
buzzer = PWMOutputDevice(12)

# Notas musicales (frecuencias en Hz)
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

# Duraciones musicales en relación al beat
BPM = 120
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
    # 1. "Noche de paz"
    ('Sol5', 'qd', 'No'), ('La5', 'e', 'che'), ('Sol5', 'q', 'de'),
    ('Mi5', 'hd', 'paz'),

    # 2. "noche de amor"
    ('Sol5', 'qd', 'No'), ('La5', 'e', 'che'), ('Sol5', 'q', 'de_a'),
    ('Mi5', 'hd', 'mor'),

    # 3. "todo duerme en derredor"
    ('Re6', 'h', 'to'), ('Re6', 'q', 'do'), ('Si5', 'h', 'duer'),
    ('Si5', 'q', 'me_en'), ('Do6', 'h', 're'), ('Do6', 'q', 'den'),
    ('Sol5', 'hd', 'dor'), 

    # 4. "entre los astros que esparcen su luz"
    ('La5', 'h', 'en'), ('La5', 'q', 'tre_los'), ('Do6', 'qd', 'as'),
    ('Si5', 'e', 'tros'), ('La5', 'q', 'que_es'), ('Sol5', 'qd', 'par'),
    ('La5', 'e', 'cen'), ('Sol5', 'q', 'su'), ('Mi5', 'hd', 'luz'),


    # 5. "bella, anunciando al niño Jesús"
    ('La5', 'h', 'be'), ('La5', 'q', 'lla_anun'), ('Do6', 'qd', 'cian'),
    ('Si5', 'e', 'do'), ('La5', 'q', 'al'), ('Sol5', 'qd', 'ni'),
    ('La5', 'e', '\x00o'), ('Sol5', 'q', 'Je'), ('Mi5', 'hd', 'sus'),
    
    # 6. "brilla en la noche de paz"
    ('Re6', 'qd', 'be'), ('Re6', 'e', 'lla_anun'), ('Re6', 'q', 'cian'),
    ('Fa6', 'qd', 'do'), ('Re6', 'e', 'al'), ('Si6', 'q', 'ni'),
    ('Do6', 'hd', '\x00o'), ('Mi5', 'hd', 'Je'),
    # 7. "brilla la estrella de paz"
    ('Do6', 'qd', 'be'), ('Sol5', 'e', 'lla_anun'), ('Mi5', 'q', 'cian'),
    ('Sol5', 'qd', 'do'), ('Fa5', 'e', 'al'), ('Re5', 'q', 'ni'),
    ('Do5', 'hd', '\x00o')
]

# Número de repeticiones de la canción
REPETICIONES = 1

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
def fade_to_color_async(r, g, b, steps=20, delay=0.01):
    def fade():
        start_r = led_red.value
        start_g = led_green.value
        start_b = led_blue.value

        for i in range(steps + 1):
            factor = i / steps
            current_r = start_r + (r - start_r) * factor
            current_g = start_g + (g - start_g) * factor
            current_b = start_b + (b - start_b) * factor
            set_color(current_r, current_g, current_b)
            sleep(delay)

    threading.Thread(target=fade, daemon=True).start()
# Reproduce una nota con duración y LEDs
def play_note(note, figure, lyric):
    duration = dur[figure] * BEAT
    freq = notas_latinas[note]

    #print(f"Tocando: {note} ({figure}) - {duration:.2f}s \n{lyric}")
    # Mostrar la información en el LCD
    lcd.clear()
    lcd.message = f"{note},({figure} - {duration:.2f}s)\n{lyric}"
    if freq == 0:
        buzzer.off()
        fade_to_color_async(0, 0, 0)
        sleep(duration)
        return

    buzzer.frequency = freq
    buzzer.value = 0.5

    # Cambiar color en cada nota (arcoíris)
    r, g, b = rainbow_color()
    fade_to_color_async(r, g, b)

    sleep(duration)
    buzzer.off()
    fade_to_color_async(0, 0, 0)
    sleep(0.05)

# Reproducción principal
try:
    for _ in range(REPETICIONES):
        for note, figure, lyric in melody:
            play_note(note, figure, lyric)

except KeyboardInterrupt:
    #print("\nInterrumpido por el usuario.")
    lcd.clear()
    lcd.message = "Interrumpido."
    lcd.clear()

finally:
    buzzer.off()
    set_color(0, 0, 0)
    #print("GPIO liberado. ¡Feliz Navidad! 🎄")
    lcd.clear()
    lcd.message = "GPIO liberado.\n\x01Feliz Navidad!"
    sleep(3)
    lcd.clear()
    lcd.message = "Noche de paz \ncompleto."
    sleep(3)
    lcd.clear()
