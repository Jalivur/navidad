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
    0b10000,
    0b11110,
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
BEAT = 90 / BPM  # Una negra

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
    ('Fa5', 'qd', 'No'), ('Sol5', 'e', 'che'), ('Fa5', 'q', 'de'),
    ('Re5', 'hd', 'paz'),

    # 2. "noche de amor"
    ('Fa5', 'qd', 'No'), ('Sol5', 'e', 'che'), ('Fa5', 'q', 'de_a'),
    ('Re5', 'hd', 'mor'),

    # 3. "todo duerme en derredor"
    ('Do6', 'h', 'to'), ('Do6', 'q', 'do'), ('La5', 'hd', 'duerme'),
    ('La#5', 'h', 'al_re'), ('La#5', 'q', 'de'), ('Fa5', 'h', 'dor'),
    ('R', 'q', ''), 

    # 4. "solo se escucha en un pobre portal"
    ('Sol5', 'h', 'Solo'), ('Sol5', 'q', 'se'), ('La#5', 'qd', 'escucha'),
    ('La5', 'e', 'en'), ('Sol5', 'q', 'un'), ('Fa5', 'qd', 'pob'),
    ('Sol5', 'e', 'bre'), ('Fa5', 'q', 'por'), ('Re5', 'h', 'tal'),
    ('R', 'q', ''),

    # 5. "De una Doncella la voz Celestial."
    ('Sol5', 'h', 'De_una'), ('Sol5', 'q', 'don'), ('La#5', 'qd', 'ce'),
    ('La5', 'e', 'lla'), ('Sol5', 'q', 'la'), ('Fa5', 'qd', 'voz'),
    ('Sol5', 'e', 'ce'), ('Fa5', 'q', 'les'), ('Re5', 'hd', 'tial'),
    
    # 6. "Duerme, mi dulce Jesús"
    ('Do6', 'h', 'Duer'), ('Do6', 'q', 'me_mi'), ('Re#6', 'qd', 'dul'),
    ('Do6', 'e', 'ce'), ('La5', 'q', 'Je'), ('La#5', 'hd', 'su_'),
    ('Re6', 'h', 'us'), ('R', 'q', ''),
    # 7. "Duerme, mi dulce Jesús."
    ('La#5', 'qd', 'Duer'), ('Fa5', 'e', 'me'), ('Re5', 'q', 'mi'),
    ('Fa5', 'qd', 'dul'), ('Re#5', 'e', 'ce'), ('Do5', 'q', 'Je'),
    ('La#4', 'w', 'sus'), ('R', 'q', ''), ('R', 'q', ''),
    
    # 8. "Noche de paz"
    ('Fa5', 'qd', 'No'), ('Sol5', 'e', 'che'), ('Fa5', 'q', 'de'),
    ('Re5', 'hd', 'paz'),

    # 9. "noche de amor"
    ('Fa5', 'qd', 'No'), ('Sol5', 'e', 'che'), ('Fa5', 'q', 'de_a'),
    ('Re5', 'hd', 'mor'),

    # 10. "todo duerme en derredor"
    ('Do6', 'h', 'to'), ('Do6', 'q', 'do'), ('La5', 'hd', 'duerme'),
    ('La#5', 'h', 'al_re'), ('La#5', 'q', 'de'), ('Fa5', 'h', 'dor'),
    ('R', 'q', ''), 

    # 11. "solo se escucha en un pobre portal"
    ('Sol5', 'h', 'Solo'), ('Sol5', 'q', 'se'), ('La#5', 'qd', 'escucha'),
    ('La5', 'e', 'en'), ('Sol5', 'q', 'un'), ('Fa5', 'qd', 'pob'),
    ('Sol5', 'e', 'bre'), ('Fa5', 'q', 'por'), ('Re5', 'h', 'tal'),
    ('R', 'q', ''),

    # 12. "De una Doncella la voz Celestial."
    ('Sol5', 'h', 'De_una'), ('Sol5', 'q', 'don'), ('La#5', 'qd', 'ce'),
    ('La5', 'e', 'lla'), ('Sol5', 'q', 'la'), ('Fa5', 'qd', 'voz'),
    ('Sol5', 'e', 'ce'), ('Fa5', 'q', 'les'), ('Re5', 'hd', 'tial'),
    
    # 13. "Duerme, mi dulce Jesús"
    ('Do6', 'h', 'Duer'), ('Do6', 'q', 'me_mi'), ('Re#6', 'qd', 'dul'),
    ('Do6', 'e', 'ce'), ('La5', 'q', 'Je'), ('La#5', 'hd', 'su_'),
    ('Re6', 'h', 'us'), ('R', 'q', ''),
    # 14. "Duerme, mi dulce Jesús."
    ('La#5', 'qd', 'Duer'), ('Fa5', 'e', 'me'), ('Re5', 'q', 'mi'),
    ('Fa5', 'qd', 'dul'), ('Re#5', 'e', 'ce'), ('Do5', 'q', 'Je'),
    ('La#4', 'w', 'sus'), ('R', 'q', ''), ('R', 'q', ''),
    
    #2
    # 1. "Noche de paz"
    ('Fa5', 'qd', 'No'), ('Sol5', 'e', 'che'), ('Fa5', 'q', 'de'),
    ('Re5', 'hd', 'paz'),

    # 2. "noche de luz"
    ('Fa5', 'qd', 'No'), ('Sol5', 'e', 'che'), ('Fa5', 'q', 'de'),
    ('Re5', 'hd', 'luz'),

    # 3. "Ha nacido Jesús"
    ('Do6', 'h', 'Ha'), ('Do6', 'q', 'na'), ('La5', 'hd', 'ci'),
    ('La#5', 'h', 'do'), ('La#5', 'q', 'Je'), ('Fa5', 'hd', 'sus'),

    # 4. "Pastorcillos que oís anunciar"
    ('Sol5', 'h', 'Pas'), ('Sol5', 'q', 'tor'), ('La#5', 'qd', 'ci'),
    ('La5', 'e', 'llos'), ('Sol5', 'q', 'que_o'), ('Fa5', 'qd', 'is'),
    ('Sol5', 'e', 'a'), ('Fa5', 'q', 'nun'), ('Re5', 'hd', 'ciar'),


    # 5. "No temáis cuando entréis a adorar"
    ('Sol5', 'h', 'No'), ('Sol5', 'q', 'te'), ('La#5', 'qd', 'mais'),
    ('La5', 'e', 'cuan'), ('Sol5', 'q', 'do_en'), ('Fa5', 'qd', 'treis'),
    ('Sol5', 'e', 'a'), ('Fa5', 'q', 'ado'), ('Re5', 'hd', 'rar'),
    
    # 6. "Que ha nacido el amor"
    ('Do6', 'h', 'Que'), ('Do6', 'q', 'ha_na'), ('Re#6', 'qd', 'ci'),
    ('Do6', 'e', 'do_el'), ('La5', 'q', 'a'), ('La#5', 'hd', 'mo'),
    ('Re6', 'hd', 'or'), 
    # 7. "Que ha nacido el amor."
    ('La#5', 'qd', 'Que_ha'), ('Fa5', 'e', 'na'), ('Re5', 'q', 'ci'),
    ('Fa5', 'qd', 'do'), ('Re#5', 'e', 'el'), ('Do5', 'q', 'a'),
    ('La#4', 'w', 'mor'), ('R', 'q', ''), ('R', 'q', ''),
    
    # 8. "Noche de paz"
    ('Fa5', 'qd', 'No'), ('Sol5', 'e', 'che'), ('Fa5', 'q', 'de'),
    ('Re5', 'hd', 'paz'),

    # 9. "noche de luz"
    ('Fa5', 'qd', 'No'), ('Sol5', 'e', 'che'), ('Fa5', 'q', 'de'),
    ('Re5', 'hd', 'luz'),

    # 10. "Ha nacido Jesús"
    ('Do6', 'h', 'Ha'), ('Do6', 'q', 'Na'), ('La5', 'hd', 'ci'),
    ('La#5', 'h', 'do'), ('La#5', 'q', 'Je'), ('Fa5', 'hd', 'sus'),


    # 11. "Desde el Pesebre del niño Jesús"
    ('Sol5', 'h', 'Des'), ('Sol5', 'q', 'de_el'), ('La#5', 'qd', 'Pese'),
    ('La5', 'e', 'bre'), ('Sol5', 'q', 'del'), ('Fa5', 'qd', 'ni'),
    ('Sol5', 'e', '\x00o'), ('Fa5', 'q', 'Je'), ('Re5', 'hd', 'sus'),

    # 12. "La tierra entera se llena de luz."
    ('Sol5', 'h', 'La_tie'), ('Sol5', 'q', 'rra'), ('La#5', 'qd', 'en'),
    ('La5', 'e', 'te'), ('Sol5', 'q', 'ra_se'), ('Fa5', 'qd', 'lle'),
    ('Sol5', 'e', 'na'), ('Fa5', 'q', 'de'), ('Re5', 'hd', 'luz'),
    
    # 13. "Porque ha nacido Jesús"
    ('Do6', 'h', 'Por'), ('Do6', 'q', 'que_ha'), ('Re#6', 'qd', 'naci'),
    ('Do6', 'e', 'do'), ('La5', 'q', 'Je'), ('La#5', 'hd', 'su_'),
    ('Re6', 'hd', 'us'), 
    # 14. "Entre canciones de amor.."
    ('La#5', 'qd', 'Entre'), ('Fa5', 'e', 'can'), ('Re5', 'q', 'cio'),
    ('Fa5', 'qd', 'nes'), ('Re#5', 'e', 'de'), ('Do5', 'q', 'a'),
    ('La#4', 'w', 'mor'), ('R', 'q', ''), ('R', 'q', ''),
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
