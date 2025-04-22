from gpiozero import Button
from signal import pause, SIGINT
import subprocess
import threading
import time
import os

# Definir el pin del botón (GPIO 21)
boton = Button(21, pull_up=True, bounce_time=0.2)

# Lista de scripts
scripts = [
    "/home/jalivur/Desktop/navidad/estrellita.py",
    "/home/jalivur/Desktop/navidad/jingelsbells.py",
    "/home/jalivur/Desktop/navidad/nochedepaz.py",
    "/home/jalivur/Desktop/navidad/felicidades.py"
]

ejecutando = False
tiempo_presionado = 0  # Para medir la duración de la pulsación

def ejecutar_todos():
    global ejecutando
    ejecutando = True
    for ruta in scripts:
        print(f"▶ Ejecutando: {ruta}")
        subprocess.run(["python3", ruta])
    print("✅ Todos los scripts completados.")
    ejecutando = False

def al_pulsar():
    global tiempo_presionado
    # Cuando el botón se presiona, iniciamos el temporizador
    tiempo_presionado = time.time()

def al_soltar():
    global tiempo_presionado
    # Cuando el botón se suelta, calculamos la duración de la pulsación
    duracion = time.time() - tiempo_presionado
    if duracion < 0.5:
        print("🟢 Pulsación corta detectada. Iniciando secuencia...")
        if not ejecutando:
            hilo = threading.Thread(target=ejecutar_todos)
            hilo.start()
    elif duracion > 10:
        print("🔴 Pulsación larga detectada. Cerrando programa...")
        cerrar_programa()

def cerrar_programa():
    try:
        boton.close()
    except:
        pass
    os.kill(os.getpid(), SIGINT)

# Asignar acciones al botón
boton.when_pressed = al_pulsar  # Detecta cuando se presiona
boton.when_released = al_soltar  # Detecta cuando se suelta

print("🎶 Pulsa el botón para ejecutar la secuencia completa de scripts.")
print("🔴 Mantén pulsado más de 10 segundos para salir.")
pause()

