# server_api.py

from flask import Flask, request, make_response
from datetime import datetime
import mysql.connector

app = Flask(__name__)


@app.route('/')
def home():
    return "Servidor Flask en línea"


# Configuración de base de datos en la nube
db_config = {
    'host': 'mainline.proxy.rlwy.net',
    'user': 'root',
    'password': '',
    'database': 'imagenes_db',
    'port': 38286
}


@app.route('/subir', methods=['POST'])
def subir_imagen():
    if 'imagen' not in request.files:
        return "No se envió imagen", 400

    imagen = request.files['imagen'].read()
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Imagenes (imagen, fecha) VALUES (%s, %s)", (imagen, fecha))
        conn.commit()
        cursor.close()
        conn.close()
        return "Imagen recibida y guardada", 200

    except mysql.connector.Error as err:
        print("❌ ERROR en DB:", err)  # <-- Agrega esto para ver el error real en los logs
        return f"Error en la base de datos: {err}", 500

@app.route('/foto')
def obtener_ultima_imagen():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT imagen FROM Imagenes ORDER BY fecha DESC LIMIT 1")
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            img_bytes = row[0]
            response = make_response(img_bytes)
            response.headers.set('Content-Type', 'image/jpeg')
            return response
        else:
            return "No hay imágenes disponibles", 404
    except mysql.connector.Error as err:
        return f"Error en la base de datos: {err}", 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
