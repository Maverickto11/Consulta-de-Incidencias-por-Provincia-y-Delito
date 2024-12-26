import os
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Cargar los datos al iniciar
df = pd.read_excel("delito.xlsx")

@app.route('/api/provincias', methods=['GET'])
def obtener_provincias():
    provincias = df["Provincia"].unique().tolist()
    return jsonify(provincias)

@app.route('/api/delitos', methods=['GET'])
def obtener_delitos():
    delitos = df["Delitos de mayor incidencia"].unique().tolist()
    return jsonify(delitos)

@app.route('/api/get_data', methods=['POST'])
def get_data():
    provincia = request.json.get('provincia')
    delito = request.json.get('delito')
    tipo = request.json.get('tipo')

    filtro_provincia = df["Provincia"] == provincia
    filtro_delito = df["Delitos de mayor incidencia"] == delito
    datos_filtrados = df[filtro_provincia & filtro_delito].iloc[:, 2:].T
    datos_filtrados.columns = ["Incidentes"]

    datos_filtrados.index = pd.to_datetime(datos_filtrados.index)

    if tipo == 'año':
        datos_filtrados = datos_filtrados.resample('Y').sum()
        datos_filtrados.index = datos_filtrados.index.strftime('%Y')
    else:
        datos_filtrados.index = datos_filtrados.index.strftime('%d-%m-%Y')

    datos_json = datos_filtrados.reset_index().rename(columns={'index': 'Fecha'}).to_dict(orient="records")
    return jsonify(datos_json)

@app.route('/')
def home():
    return "La API está funcionando. Accede a las rutas /api/provincias o /api/delitos."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render asigna el puerto
    app.run(host="0.0.0.0", port=port)
