import pandas as pd
import requests
import logging
from tkinter import messagebox

logging.basicConfig(level=logging.WARNING)

URL = "https://www.datos.gov.co/resource/gt2j-8ykr.json"

def obtener_datos(departamento, limite):
    """Consulta la API de COVID-19 y devuelve un DataFrame con los resultados filtrados."""
    try:
        # Parámetros para la consulta
        params = {
            "$limit": limite,
            "$select": "ciudad_municipio_nom, departamento_nom, edad, fuente_tipo_contagio, estado",
            "$where": f"lower(departamento_nom)='{departamento.lower()}'"
        }

        response = requests.get(URL, params=params)
        data = response.json()

        if not isinstance(data, list):  # Verificar si la API respondió correctamente
            raise ValueError("Respuesta inesperada de la API")

        df = pd.DataFrame(data)

        # Verificar si las columnas esperadas existen
        columnas_necesarias = ["ciudad_municipio_nom", "departamento_nom", "edad", "fuente_tipo_contagio", "estado"]
        columnas_disponibles = df.columns.tolist()

        if not all(col in columnas_disponibles for col in columnas_necesarias):
            logging.warning(f"Columnas disponibles en la API: {df.columns}")
            raise ValueError("Las columnas necesarias no están disponibles en la API.")

        # Agregar la columna "País de procedencia" con valor "No disponible"
        df["País de procedencia"] = "No disponible"

        # Renombrar columnas para que coincidan con la UI
        df = df.rename(columns={
            "ciudad_municipio_nom": "Ciudad",
            "departamento_nom": "Departamento",
            "edad": "Edad",
            "fuente_tipo_contagio": "Tipo",
            "estado": "Estado"
        })

        return df[["Ciudad", "Departamento", "Edad", "Tipo", "Estado", "País de procedencia"]]

    except Exception as e:
        logging.error(f"Error al consultar la API: {e}")
        messagebox.showerror("Error", f"No se pudo obtener los datos: {e}")
        return pd.DataFrame()  # Devolver un DataFrame vacío en caso de error