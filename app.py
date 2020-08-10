from flask import Flask, request, send_file
from apiAnalisis.modeloAnalisis import modeloAnalisis, Cliente
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/predecirCliente', methods=['POST'])
def predecirCliente():
    if request.headers['Content-Type'] == 'application/json':
        req_data = request.get_json()
        DNI = req_data['DNI']
        PLAZOMESESCREDITO = req_data['PLAZOMESESCREDITO']
        HISTORIALCREDITO = req_data['HISTORIALCREDITO']
        PROPOSITOCREDITO = req_data['PROPOSITOCREDITO']
        MONTOCREDITO = req_data['MONTOCREDITO']
        SALDOCUENTAAHORROS = req_data['SALDOCUENTAAHORROS']
        TIEMPOEMPLEO = req_data['TIEMPOEMPLEO']
        TASAPAGO = req_data['TASAPAGO']
        ESTADOCIVILYSEXO = req_data['ESTADOCIVILYSEXO']
        GARANTE = req_data['GARANTE']
        AVALUOVIVIENDA = req_data['AVALUOVIVIENDA']
        ACTIVOS = req_data['ACTIVOS']
        EDAD = req_data['EDAD']
        VIVIENDA = req_data['VIVIENDA']
        CANTIDADCREDITOSEXISTENTES = req_data['CANTIDADCREDITOSEXISTENTES']
        EMPLEO = req_data['EMPLEO']
        TRABAJADOREXTRANJERO = req_data['TRABAJADOREXTRANJERO']
        TIPOCLIENTE = req_data['TIPOCLIENTE']

        clinte = Cliente(DNI, PLAZOMESESCREDITO, HISTORIALCREDITO, PROPOSITOCREDITO, MONTOCREDITO, SALDOCUENTAAHORROS,
                         TIEMPOEMPLEO, TASAPAGO, ESTADOCIVILYSEXO, GARANTE, AVALUOVIVIENDA, ACTIVOS, EDAD, VIVIENDA,
                         CANTIDADCREDITOSEXISTENTES, EMPLEO, TRABAJADOREXTRANJERO, TIPOCLIENTE)
        modeloAnalisis.addRow(clinte, clinte)
        resul = modeloAnalisis.predecirTipoCliente(modeloAnalisis, int(DNI))
        return resul;


@app.route('/predecir', methods=['GET'])
def predecirTipoCliente():
    DNI = request.args.get('DNI')
    resul = modeloAnalisis.predecirTipoCliente(modeloAnalisis, DNI)
    return resul

@app.route('/getImage')
def getImage():
    modeloAnalisis.getImg(modeloAnalisis)
    return send_file("apiAnalisis/pastel.png", mimetype='image/png')

@app.route('/getPaste', methods=['GET'])
def getPaste():
    buenos = request.args.get('buenos')
    malos = request.args.get('malos')
    definir = request.args.get('definir')
    modeloAnalisis.getPastel(modeloAnalisis, int(buenos), int(malos), int(definir))
    return send_file("apiAnalisis/pastel2.png", mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            debug=True,
            port=8080)
