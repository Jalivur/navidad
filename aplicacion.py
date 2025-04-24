import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QColorDialog,
    QSlider, QHBoxLayout, QComboBox, QStyleFactory, QFrame, QSpinBox, QLineEdit
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPalette
from gpiozero import PWMLED
import itertools
import math
import board
import digitalio
import adafruit_character_lcd.character_lcd as character_lcd

# Configuración de LEDs
led_red = PWMLED(17)
led_green = PWMLED(27)
led_blue = PWMLED(22)

def set_color(r, g, b):
    led_red.value = r
    led_green.value = g
    led_blue.value = b

# Configuración LCD 1602
lcd_rs = digitalio.DigitalInOut(board.D26)
lcd_en = digitalio.DigitalInOut(board.D19)
lcd_d4 = digitalio.DigitalInOut(board.D13)
lcd_d5 = digitalio.DigitalInOut(board.D6)
lcd_d6 = digitalio.DigitalInOut(board.D5)
lcd_d7 = digitalio.DigitalInOut(board.D11)
lcd_columns = 16
lcd_rows = 2
lcd = character_lcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows
)
lcd.clear()

class LEDController(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de LEDs RGB")
        self.setFixedSize(400, 500)
        self.color = QColor(255, 0, 0)
        self.auto_sequence_step = 0
        self.auto_sequence_ticks = 0
        self.auto_ticks_per_effect = 25
        self.blink_state = False
        self.strobe_state = False

        self.default_colors = {
            "Destello": QColor(0, 255, 0),
            "Estroboscópico": QColor(255, 0, 255)
        }

        QApplication.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(45, 45, 45))
        palette.setColor(QPalette.AlternateBase, QColor(30, 30, 30))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(45, 45, 45))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(0, 122, 204))
        QApplication.setPalette(palette)

        self.label = QLabel("Selecciona un color:")
        self.color_btn = QPushButton("Elegir color")
        self.color_btn.clicked.connect(self.choose_color)

        self.intensity_label = QLabel("Intensidad:")
        self.intensity_slider = QSlider(Qt.Horizontal)
        self.intensity_slider.setRange(0, 100)
        self.intensity_slider.setValue(100)
        self.intensity_slider.valueChanged.connect(self.update_led)

        self.mode_label = QLabel("Modo automático:")
        self.mode_selector = QComboBox()
        self.modes = [
            "Manual", "Arcoíris", "Destello", "Fade Loop", "Estroboscópico",
            "Pulso Senoidal", "Secuencia Automática", "Ciclico RGB"
        ]
        self.mode_selector.addItems(self.modes)
        self.mode_selector.currentTextChanged.connect(self.change_mode)

        self.speed_label = QLabel("Velocidad (ms):")
        self.speed_spinner = QSpinBox()
        self.speed_spinner.setRange(50, 2000)
        self.speed_spinner.setValue(200)
        self.speed_spinner.valueChanged.connect(self.update_timer)

        self.duration_label = QLabel("Duración por efecto (segundos):")
        self.duration_spinner = QSpinBox()
        self.duration_spinner.setRange(1, 60)
        self.duration_spinner.setValue(35)
        self.duration_spinner.valueChanged.connect(self.update_duration)

        self.lcd_label = QLabel("Mensaje en LCD:")
        self.lcd_input = QLineEdit()
        self.lcd_input.setPlaceholderText("Escribe un mensaje")
        self.lcd_input.returnPressed.connect(self.update_lcd)
        self.lcd_btn = QPushButton("Enviar a LCD")
        self.lcd_btn.clicked.connect(self.update_lcd)

        self.backout_btn = QPushButton("Apagar Todo")
        self.backout_btn.clicked.connect(self.backout)

        self.auto_timer = QTimer()
        self.auto_timer.timeout.connect(self.run_mode)

        self.color_cycle = itertools.cycle([
            (1.0, 0.0, 0.0), (1.0, 0.5, 0.0), (1.0, 1.0, 0.0),
            (0.5, 1.0, 0.0), (0.0, 1.0, 0.0), (0.0, 1.0, 0.5),
            (0.0, 1.0, 1.0), (0.0, 0.5, 1.0), (0.0, 0.0, 1.0),
            (0.5, 0.0, 1.0), (1.0, 0.0, 1.0), (1.0, 0.0, 0.5),
            (0.8, 0.2, 0.6), (0.6, 0.4, 0.8), (0.3, 0.3, 1.0),
            (0.2, 0.6, 1.0), (0.1, 0.9, 0.5), (0.9, 0.9, 0.3),
            (1.0, 0.8, 0.1), (0.7, 0.3, 0.2), (0.4, 0.2, 0.1), 
            (0.2, 0.1, 0.3), (0.1, 0.2, 0.4), (0.3, 0.5, 0.6),
            (0.5, 0.7, 0.8), (0.7, 0.9, 1.0), (1.0, 1.0, 1.0), 
            (0.9, 0.8, 0.7), (0.7, 0.6, 0.5), (0.5, 0.4, 0.3),
            (0.3, 0.2, 0.1), (0.1, 0.1, 0.1), (0.2, 0.2, 0.2),
            (0.4, 0.4, 0.4), (0.6, 0.6, 0.6), (0.8, 0.8, 0.8)
        ])

        self.rgb_cycle_order = ["RGB", "RBG", "GRB", "GBR", "BRG", "BGR"]
        self.rgb_order_selector = QComboBox()
        self.rgb_order_selector.addItems(self.rgb_cycle_order)
        self.rgb_order_selector.currentTextChanged.connect(self.update_rgb_order)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.color_btn)
        layout.addWidget(self.intensity_label)
        layout.addWidget(self.intensity_slider)
        layout.addWidget(self.mode_label)
        layout.addWidget(self.mode_selector)
        layout.addWidget(self.speed_label)
        layout.addWidget(self.speed_spinner)
        layout.addWidget(self.duration_label)
        layout.addWidget(self.duration_spinner)
        layout.addWidget(self.lcd_label)
        layout.addWidget(self.lcd_input)
        layout.addWidget(self.lcd_btn)
        layout.addWidget(self.rgb_order_selector)
        layout.addWidget(self.backout_btn)
        self.setLayout(layout)

        self.update_led()

    def choose_color(self):
        self.color = QColorDialog.getColor()
        if self.color.isValid():
            self.update_led()

    def update_led(self):
        if self.mode_selector.currentText() != "Manual":
            return
        r = self.color.red() / 255.0
        g = self.color.green() / 255.0
        b = self.color.blue() / 255.0
        intensity = self.intensity_slider.value() / 100.0
        set_color(r * intensity, g * intensity, b * intensity)

    def change_mode(self, mode):
        if mode in self.default_colors:
            self.color = self.default_colors[mode]
        if mode == "Manual":
            self.auto_timer.stop()
            self.update_led()
        else:
            self.update_timer()

    def update_timer(self):
        interval = self.speed_spinner.value()
        self.auto_timer.setInterval(interval)
        if self.mode_selector.currentText() != "Manual":
            self.auto_timer.start()

    def update_duration(self):
        self.auto_ticks_per_effect = (1000 // self.speed_spinner.value()) * self.duration_spinner.value()

    def run_mode(self):
        mode = self.mode_selector.currentText()
        intensity = self.intensity_slider.value() / 100.0

        # Solo actualizar LCD si cambia de modo
        if mode != getattr(self, "last_lcd_mode", ""):
            lcd.clear()
            lcd.message = mode[:16]
            self.last_lcd_mode = mode

        if mode == "Secuencia Automática":
            all_effects = ["Arcoíris", "Fade Loop", "Destello", "Estroboscópico", "Pulso Senoidal"]
            if self.auto_sequence_ticks == 0:
                self.current_auto_effect = all_effects[self.auto_sequence_step % len(all_effects)]
                self.auto_sequence_step += 1

            # Actualizar el LCD con el efecto real en Secuencia Automática
            if self.current_auto_effect != getattr(self, "last_lcd_mode_effect", ""):
                lcd.clear()
                lcd.message = self.current_auto_effect[:16]
                self.last_lcd_mode_effect = self.current_auto_effect

            self.run_effect(self.current_auto_effect, intensity)

            self.auto_sequence_ticks += 1
            if self.auto_sequence_ticks >= self.auto_ticks_per_effect:
                self.auto_sequence_ticks = 0
        else:
            self.run_effect(mode, intensity)

    def run_effect(self, mode, intensity):
        r = self.color.red() / 255.0
        g = self.color.green() / 255.0
        b = self.color.blue() / 255.0

        if mode == "Arcoíris":
            r, g, b = next(self.color_cycle)
            set_color(r * intensity, g * intensity, b * intensity)

        elif mode == "Destello":
            self.blink_state = not getattr(self, 'blink_state', False)
            if self.blink_state:
                set_color(r * intensity, g * intensity, b * intensity)
            else:
                set_color(0, 0, 0)

        elif mode == "Fade Loop":
            self.fade_phase = getattr(self, 'fade_phase', 0)
            self.fade_phase = (self.fade_phase + 1) % 300
            phase = self.fade_phase
            if phase < 100:
                r, g, b = 1.0 - phase / 100.0, phase / 100.0, 0.0
            elif phase < 200:
                r, g, b = 0.0, 1.0 - (phase - 100) / 100.0, (phase - 100) / 100.0
            else:
                r, g, b = (phase - 200) / 100.0, 0.0, 1.0 - (phase - 200) / 100.0
            set_color(r * intensity, g * intensity, b * intensity)

        elif mode == "Estroboscópico":
            self.strobe_state = not self.strobe_state
            if self.strobe_state:
                set_color(r * intensity, g * intensity, b * intensity)
            else:
                set_color(0, 0, 0)

        elif mode == "Pulso Senoidal":
            self.pulse_step = getattr(self, 'pulse_step', 0)
            self.pulse_step += 1
            val = (math.sin(self.pulse_step / 10.0) + 1) / 2.0 * intensity
            set_color(r * val, g * val, b * val)

        elif mode == "Ciclico RGB":
            self.rgb_cycle_step = getattr(self, 'rgb_cycle_step', 0)
            self.rgb_cycle_step = (self.rgb_cycle_step + 1) % len(self.rgb_cycle_order)
            order = self.rgb_cycle_order[self.rgb_cycle_step]
            if order == "RGB":
                set_color(r * intensity, g * intensity, b * intensity)
            elif order == "RBG":
                set_color(r * intensity, b * intensity, g * intensity)
            elif order == "GRB":
                set_color(g * intensity, r * intensity, b * intensity)
            elif order == "GBR":
                set_color(g * intensity, b * intensity, r * intensity)
            elif order == "BRG":
                set_color(b * intensity, r * intensity, g * intensity)
            elif order == "BGR":
                set_color(b * intensity, g * intensity, r * intensity)

    def update_rgb_order(self):
        # Actualizar el orden RGB cuando cambie el selector.
        pass

    def update_lcd(self):
        lcd.clear()
        lcd.message = self.lcd_input.text()

    def backout(self):
        set_color(0, 0, 0)
        lcd.clear()
    def closeEvent(self, event):
    # Limpiar el LCD al cerrar la ventana
        lcd.clear()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LEDController()
    window.show()
    sys.exit(app.exec())
