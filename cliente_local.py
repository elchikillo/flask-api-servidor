# cliente_local.py

import serial
import time
import requests
import cv2
from datetime import datetime

def tomar_foto():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()

    if not ret:
        print("Error al capturar la imagen")
        return None

    ret2, buffer = cv2.imencode('.jpg', frame)
    if not ret2:
        print("Error al codificar la imagen")
        return None

    return buffer.tobytes()

def enviar_imagen_al_servidor(img_bytes):
    try:
        response = requests.post(
            'https://TU_SERVIDOR_RENDER.com/subir',  # cambiar más adelante
            files={'imagen': ('foto.jpg', img_bytes, 'image/jpeg')}
        )
        print("Respuesta del servidor:", response.status_code)
    except Exception as e:
        print("Error al enviar imagen:", e)

def escuchar_serial():
    ser = serial.Serial('COM3', 9600)
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line == "MOTION_DETECTED":
                print("Movimiento detectado. Tomando y enviando imagen...")
                imagen = tomar_foto()
                if imagen:
                    enviar_imagen_al_servidor(imagen)

if __name__ == '__main__':
    escuchar_serial()
