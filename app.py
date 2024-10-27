<<<<<<< HEAD
import os
=======
>>>>>>> e0837399f0e720292cae0cf9bc7afd11e6fd45b2
from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Cargar los datos al iniciar
df = pd.read_excel("delito.xlsx")

@app.route('/')
def index():
    # Obtener provincias y delitos únicos para pasarlos al HTML
    provincias = df["Provincia"].unique().tolist()
    delitos = df["Delitos de mayor incidencia"].unique().tolist()
    return render_template('index.html', provincias=provincias, delitos=delitos)

@app.route('/get_data', methods=['POST'])
def get_data():
    # Obtener los parámetros enviados desde el frontend
    provincia = request.json.get('provincia')
    delito = request.json.get('delito')
    tipo = request.json.get('tipo')
    
    # Filtrar los datos
    filtro_provincia = df["Provincia"] == provincia
    filtro_delito = df["Delitos de mayor incidencia"] == delito
    datos_filtrados = df[filtro_provincia & filtro_delito].iloc[:, 2:].T  # Tomar columnas de meses
    datos_filtrados.columns = ["Incidentes"]
    
    # Convertir el índice en formato de fecha
    datos_filtrados.index = pd.to_datetime(datos_filtrados.index)

    # Agrupar los datos según la opción seleccionada (mes o año)
    if tipo == 'año':
        datos_filtrados = datos_filtrados.resample('Y').sum()
        datos_filtrados.index = datos_filtrados.index.strftime('%Y')
    else:
        datos_filtrados.index = datos_filtrados.index.strftime('%d-%m-%Y')
    
    # Convertir los datos a JSON
    datos_json = datos_filtrados.reset_index().rename(columns={'index': 'Fecha'}).to_dict(orient="records")
    
    return jsonify(datos_json)

if __name__ == "__main__":
<<<<<<< HEAD
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
=======
    app.run(debug=True)
>>>>>>> e0837399f0e720292cae0cf9bc7afd11e6fd45b2
