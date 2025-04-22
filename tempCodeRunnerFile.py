from gpiozero import Button
from signal import pause
import subprocess
import time
import threading

# Definir el pin del botón (ejemplo: GPIO 21)
boton = Button(21, pull_up=True, bounce_time=0.2)

# Lista de rutas a tus scripts
scripts = [
    "/home/jalivur/Desktop/navidad/estrellita.py",
    "/home/jalivur/Desktop/navidad/jingelsbells.py",
    "/home/jalivur/Desktop/navidad/nochedepaz.py",
    "/home/jalivur/Desktop/navidad/felicidades.py"
]

ejecutando = False  # flag para evitar múltiples pulsaciones simultáneas

def ejecutar_todos():
    global ejecutando
    ejecutando = True
    for ruta in scripts:
        print(f"▶ Ejecutando: {ruta}")
        subprocess.run(["python3", ruta])
    print("✅ Todos los scripts completados.")
    ejecutando = False
    return

def al_pulsar():
    global ejecutando
    if not ejecutando:
        print("🟢 Pulsado. Iniciando secuencia...")
        hilo = threading.Thread(target=ejecutar_todos)
        hilo.start()
    else:
        print("⚠️ Ya se está ejecutando una secuencia.")

boton.when_pressed = al_pulsar

print("🎶 Pulsa el botón para ejecutar la secuencia completa de scripts.")
pause()