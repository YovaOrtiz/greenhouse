from datetime import datetime

from flask import Flask, jsonify

app = Flask(__name__)

# nombre dde la variable = valor de la variable
# esta variable es global
estado_sistema = "apagado"
consumo_luz = 0

nombre_archivo_control = "invernadero.txt"

@app.route('/')
def hello_world():  # put application's code here
    return 'Invernadero inteligente!'


@app.get("/datos")
def obtener_datos_generales():
    #if estado_sistema != "Encendido":
    #    return jsonify(mensaje="Errror al obtener datos sistemas apagado"), 500

    print("Obteniendo temperatura")
    lectura = {'temperatura':34, 'humedad':22, 'viento':"32km","hora": str(datetime.now())}
    with  open(nombre_archivo_control, "a") as file:
        file.write(str(lectura) + "\n")
    return  jsonify(lectura)

@app.get("/apagado")
def apagar_sistema():
    global  estado_sistema
    print("Apagando sistema")
    estado_sistema = "apagado"
    return jsonify(mensaje="sistema apagado con exito")


@app.get("/encender")
def encender_sistemas():
    global estado_sistema
    print("encender sistemas")
    estado_sistema = "Encendido"
    return jsonify(mensaje="sistema encendido con exito")

@app.get("/humedad")
def optener_humedad():

    print("Obteniendo humedad")
    lectura = {"humedad":22}

    return  jsonify(lectura)

@app.get("/temperatura")
def optener_temperatura():


    lectura = {"temperatura":34}

    return  jsonify(lectura)

@app.get("/viento")
def optener_viento():

    lectura = {'viento':"32km"}

    return  jsonify(lectura)






if __name__ == '__main__':
    app.run(port=5000)
