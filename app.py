from datetime import datetime
import random
import threading
import time
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__)

# Variables globales
estado_sistema = "apagado"
nombre_archivo_control = "invernadero.txt"

# Simulación de zonas con sus niveles de humedad y estado de riego
zonas = {
    "zona_1": {"humedad": 0, "riego": False},
    "zona_2": {"humedad": 0, "riego": False},
    "zona_3": {"humedad": 0, "riego": False}
}

@app.route('/')
def home():
    return 'Bienvenido al Invernadero Inteligente!'

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico')

@app.route('/general')
def hello_world():
    return 'Invernadero inteligente!'

def generar_datos_aleatorios():
    temperatura = random.uniform(15, 35)  # Temperatura entre 15 y 35 grados
    humedad = random.uniform(20, 80)  # Humedad entre 20 y 80%
    viento = random.uniform(5, 50)  # Velocidad del viento entre 5 y 50 km/h
    return {
        'temperatura': round(temperatura, 2),
        'humedad': round(humedad, 2),
        'viento': f"{round(viento, 2)}km",
        "hora": str(datetime.now())
    }

def generar_datos_zona():
    for zona in zonas:
        zonas[zona]["humedad"] = round(random.uniform(20, 80), 2)

@app.get("/datos")
def obtener_datos_generales():
    print("Obteniendo temperatura")
    lectura = generar_datos_aleatorios()
    with open(nombre_archivo_control, "a") as file:
        file.write(str(lectura) + "\n")
    return jsonify(lectura)

@app.get("/zonas")
def obtener_datos_zonas():
    if estado_sistema != "Encendido":
        return jsonify(mensaje="Error al obtener datos, sistema apagado"), 500

    generar_datos_zona()
    with open(nombre_archivo_control, "a") as file:
        file.write(str(zonas) + "\n")
    return jsonify(zonas)

@app.get("/apagado")
def apagar_sistema():
    global estado_sistema
    print("Apagando sistema")
    estado_sistema = "apagado"
    return jsonify(mensaje="sistema apagado con exito")

@app.get("/encender")
def encender_sistemas():
    global estado_sistema
    print("Encender sistemas")
    estado_sistema = "Encendido"
    return jsonify(mensaje="sistema encendido con exito")

@app.get("/control_riego")
def controlar_riego():
    if estado_sistema != "Encendido":
        return jsonify(mensaje="Error al controlar riego, sistema apagado"), 500

    print("Verificando necesidad de riego en las zonas")
    generar_datos_zona()
    acciones = {}
    for zona, datos in zonas.items():
        if datos["humedad"] < 35:
            datos["riego"] = True
            acciones[zona] = "Riego activado"
        else:
            datos["riego"] = False
            acciones[zona] = "Riego no necesario"

    acciones['hora'] = str(datetime.now())
    with open(nombre_archivo_control, "a") as file:
        file.write(str(acciones) + "\n")
    return jsonify(acciones)

def verificar_humedad():
    while True:
        if estado_sistema == "Encendido":
            generar_datos_zona()
            acciones = {}
            for zona, datos in zonas.items():
                if datos["humedad"] < 35 and not datos["riego"]:
                    datos["riego"] = True
                    acciones[zona] = "Riego activado"
                elif datos["humedad"] >= 35 and datos["riego"]:
                    datos["riego"] = False
                    acciones[zona] = "Riego desactivado"
                else:
                    acciones[zona] = "Riego no necesario"

            acciones['hora'] = str(datetime.now())
            with open(nombre_archivo_control, "a") as file:
                file.write(str(acciones) + "\n")
            print(acciones)
        time.sleep(60)

if __name__ == '__main__':
    # Iniciar el hilo de verificación de humedad
    thread = threading.Thread(target=verificar_humedad)
    thread.daemon = True
    thread.start()

    app.run(port=5000)
