"""Este script obtiene las tendencias de búsqueda actuales en Bing para un país o región específica. Utiliza la API de Bing News Search para obtener las tendencias de búsqueda actuales en un país o región específica."""

import requests
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Lista de códigos de países para América
country_codes = {
    'argentina': 'es-AR',
    'bolivia': 'es-BO',
    'brazil': 'pt-BR',
    'canada': 'en-CA',
    'chile': 'es-CL',
    'colombia': 'es-CO',
    'costa rica': 'es-CR',
    'cuba': 'es-CU',
    'dominican republic': 'es-DO',
    'ecuador': 'es-EC',
    'el salvador': 'es-SV',
    'guatemala': 'es-GT',
    'honduras': 'es-HN',
    'mexico': 'es-MX',
    'nicaragua': 'es-NI',
    'panama': 'es-PA',
    'paraguay': 'es-PY',
    'peru': 'es-PE',
    'puerto rico': 'es-PR',
    'united states': 'en-US',
    'uruguay': 'es-UY',
    'venezuela': 'es-VE'
}


def get_bing_trending_searches(region):
    """
    Obtiene las tendencias de búsqueda actuales en Bing para una región específica.

    Parámetros:
    region (str): Código del país o región (por ejemplo, 'es-CO' para Colombia, 'en-US' para Estados Unidos).
    """
    api_key = os.getenv('BING_API_KEY')
    if not api_key:
        raise ValueError(
            "La clave de API de Bing no está configurada en el archivo .env")

    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
    }
    params = {
        'mkt': region,
    }
    response = requests.get(
        'https://api.bing.microsoft.com/v7.0/news/trendingtopics', headers=headers, params=params)
    response.raise_for_status()
    trending_searches = response.json()

    # Imprime las diez primeras tendencias de búsqueda numeradas
    for i, trend in enumerate(trending_searches['value'][:10], start=1):
        print(f"{i}. {trend['name']}")


if __name__ == "__main__":
    # Solicita al usuario que ingrese el nombre del país o región
    country_name = input(
        "Ingrese el nombre del país o región (por ejemplo, 'colombia', 'united states'): ").strip().lower()

    # Obtiene el código del país o región
    region_code = country_codes.get(country_name)
    if not region_code:
        print("País o región no válido.")
    else:
        # Consulta las tendencias de búsqueda en Bing para la región ingresada
        get_bing_trending_searches(region_code)
