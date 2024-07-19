from datetime import datetime
import random
from flask import Flask, jsonify

app = Flask(__name__)

# nombre de la variable = valor de la variable
# esta variable es global
estado_sistema = "apagado"
consumo_luz = 0

nombre_archivo_control = "invernadero.txt"


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


@app.get("/datos")
def obtener_datos_generales():
    # if estado_sistema != "Encendido":
    #    return jsonify(mensaje="Error al obtener datos, sistema apagado"), 500

    print("Obteniendo temperatura")
    lectura = generar_datos_aleatorios()
    with open(nombre_archivo_control, "a") as file:
        file.write(str(lectura) + "\n")
    return jsonify(lectura)


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

    print("Verificando necesidad de riego")
    datos = generar_datos_aleatorios()
    if datos['humedad'] < 35:
        accion = "Riego activado"
    else:
        accion = "Riego no necesario"

    datos['accion'] = accion
    with open(nombre_archivo_control, "a") as file:
        file.write(str(datos) + "\n")
    return jsonify(datos)


if __name__ == '__main__':
    app.run(port=5000)

