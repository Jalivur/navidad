from gpiozero import PWMLED, PWMOutputDevice
from time import sleep
import random
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
# Caracteres personalizados
custom_ñ = [
    0b00100,
    0b01010,
    0b10000,
    0b01110,
    0b10001,
    0b10001,
    0b10001,
    0b00000
]
lcd.create_char(0, custom_ñ)

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
lcd.create_char(1, custom_ex)

# GPIO setup
led_red = PWMLED(17)
led_green = PWMLED(27)
led_blue = PWMLED(22)
buzzer = PWMOutputDevice(12)

# Notas musicales (frecuencias aproximadas)
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

# Duraciones musicales
BPM = 100
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

# Almacenar el último color
last_color = [0, 0, 0]

def generate_new_color():
    global last_color
    new_color = [
        random.uniform(0.0, 1.0),
        random.uniform(0.0, 1.0),
        random.uniform(0.0, 1.0)
    ]
    # Asegurarse de que el nuevo color sea diferente
    while new_color == last_color:
        new_color = [
            random.uniform(0.0, 1.0),
            random.uniform(0.0, 1.0),
            random.uniform(0.0, 1.0)
        ]
    last_color = new_color
    return new_color

# Funciones
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

def play_note(note, figure, lyric):
    duration = dur[figure] * BEAT
    freq = notas_latinas[note]
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

    r, g, b = generate_new_color()
    fade_to_color_async(r, g, b)

    sleep(duration)
    buzzer.off()
    fade_to_color_async(0, 0, 0)
    sleep(0.05)



# 🎶 Juntar todo
melody = (
    # “Campana sobre campana”
    ('Fa5', 'q', 'Cam'), ('Fa5', 'e', 'pa'), ('Fa5', 'e', 'na'), 
    ('Fa5', 'q', 'so'),('Mi5', 'e', 'bre'), ('Fa5', 'e', 'cam'), 
    ('Sol5', 'qd', 'pa-'), ('Mi5', 'e', 'a'),('Do5', 'q', 'na'),
    
    # “y sobre campana una.”
    ('Sol5', 'q', 'y'), ('Sol5','e','so'), ('La5','e','bre'),
    ('La#5', 'q', 'cam'), ('La5','e','pa'), ('Sol5','e','na'),
    ('La5','qd','u-'), ('Sol5','e','u'), ('Fa5','h','na'),
    
    # “Asomate a la ventana”
    ('Fa5', 'q', 'A'), ('Fa5', 'e', 'so'), ('Fa5', 'e', 'ma'), 
    ('Fa5', 'q', 'te'),('Mi5', 'e', 'A'), ('Fa5', 'e', 'La'), 
    ('Sol5', 'qd', 'Venta-'), ('Mi5', 'e', 'a'),('Do5', 'q', 'na'),
    
    # “Veras al Niño en la cuna”
    ('Sol5', 'q', 'Ve'), ('Sol5','e','ras'), ('La5','e','al'),
    ('La#5', 'q', 'Ni\x00o'), ('La5','e','en'), ('Sol5','e','la'),
    ('La5','qd','cu-'), ('Sol5','e','u'), ('Fa5','q','na'),
    ('R', 'e', ''),
    
    # “Belen, campanas de belen”
    ('La5', 'e', 'Be'), ('Do6', 'qd', 'len'), ('Do6', 'e', 'Cam'), 
    ('Re6', 'e', 'pa'),('Do6', 'e', 'nas'), ('La#5', 'e', 'De'), 
    ('Re6', 'e', 'Be'), ('Do6', 'qd', 'len'),
    
    #"Que los Angeles tocan"
    ('Do6', 'e', 'Que'), ('Re6', 'e', 'Los'), ('Do6', 'e', 'An'), 
    ('Re6', 'e', 'Ge'),('Mi6', 'e', 'les'), ('Fa6', 'e', 'To-'), 
    ('Do6', 'e', 'o'), ('La5', 'e', 'can'),
    
    #"Que nuevas nos traeis"
    ('Re6', 'e', 'Que'), ('Do6', 'e', 'Nue'), ('La#5', 'e', 'vas'), 
    ('La5', 'e', 'Nos'),('Sol5', 'e', 'Tra'), ('Fa5', 'h', 'eis'),
    
    #"Recogido Tu Rebaño"
    ('La5', 'qd', 'Re'), ('La#5', 'e', 'co'), ('La5', 'e', 'gi-'), 
    ('Sol5', 'e', 'i'),('Fa5', 'q', 'do'), ('Do6', 'qd', 'Tu'),
    ('Re6', 'e', 'Re'), ('Do6', 'e', 'Ba-'), ('La#5', 'e', 'a'),
    ('La5', 'q', '\x00o'),
    
    #"A Donde Vas Pastorcito"
    ('Do6', 'qd', 'A'), ('Do6', 'e', 'Don'), ('Si5', 'qd', 'de'), 
    ('Sol5', 'e', 'Vas'),('Do6', 'qd', 'Pas'), ('La#5', 'e', 'tor'),
    ('La5', 'e', 'ci-'), ('Sol5', 'e', 'i'), ('Fa5', 'q', 'to'),
    
    #"Voy a llevar al portal"
    ('La5', 'qd', 'Voy'), ('La#5', 'e', 'a'), ('La5', 'e', 'lle-'), 
    ('Sol5', 'e', 'e'),('Fa5', 'q', 'var'), ('Do6', 'qd', 'al'),
    ('Re6', 'e', 'Por'), ('Do6', 'e', 'ta-'), ('La#5', 'e', 'a'),
    ('La5', 'q', 'al'),
    
    #"Requeson Manteca y Vino"
    ('Do6', 'qd', 'Re'), ('Do6', 'e', 'que'), ('Si5', 'qd', 'son'), 
    ('Sol5', 'e', 'Man'),('Do6', 'qd', 'te'), ('La#5', 'e', 'ca y'),
    ('La5', 'e', 'Vi-'), ('Sol5', 'e', 'i'), ('Fa5', 'e', 'no'),
    
    #“Belen, campanas de belen”
    ('La5', 'e', 'Be'), ('Do6', 'qd', 'len'), ('Do6', 'e', 'Cam'), 
    ('Re6', 'e', 'pa'),('Do6', 'e', 'nas'), ('La#5', 'e', 'De'), 
    ('Re6', 'e', 'Be'), ('Do6', 'qd', 'len'),
    
    #"Que los Angeles tocan"
    ('Do6', 'e', 'Que'), ('Re6', 'e', 'Los'), ('Do6', 'e', 'An'), 
    ('Re6', 'e', 'Ge'),('Mi6', 'e', 'les'), ('Fa6', 'e', 'To-'), 
    ('Do6', 'e', 'o'), ('La5', 'e', 'can'),
    
    #"Que nuevas nos traeis"
    ('Re6', 'e', 'Que'), ('Do6', 'e', 'Nue'), ('La#5', 'e', 'vas'), 
    ('La5', 'e', 'Nos'),('Sol5', 'e', 'Tra'), ('Fa5', 'h', 'eis'),
)

# ▶️ Reproducir
try:
    for note, figure, lyric in melody:
        play_note(note, figure, lyric)
except KeyboardInterrupt:
    #print("Interrumpido.")
    lcd.clear()
    lcd.message = "Interrumpido."
    sleep(3)
    lcd.clear()
finally:
    buzzer.off()
    set_color(0, 0, 0)
    lcd.clear()
    lcd.message = "Campana \nSobre Campana"
    sleep(3)
    lcd.clear()
    lcd.message = "Terminado"
    sleep(3)
    lcd.clear()
