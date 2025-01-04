"""
Este script obtiene las tendencias de búsqueda actuales en Bing para un país o región específica. Utiliza la API de Bing News Search para obtener las tendencias de búsqueda actuales en un país o región específica.
""" # pylint: disable=line-too-long

import os
import requests
from dotenv import load_dotenv  # cSpell:ignore dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()  # cSpell:ignore dotenv

# Lista de códigos de países para América
# cSpell: ignore bolivia, brazil, canada, chile, colombia, costa, cuba, dominican, ecuador, el, guatemala, honduras, mexico, nicaragua, panama, paraguay, peru, puerto, uruguay, venezuela # pylint: disable=line-too-long
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
    Obtiene las tendencias de búsqueda actuales en Bing para un país específica.

    Parámetros:
    region (str): Código del país (por ejemplo, 'es-CO' para Colombia, 'en-US' para Estados Unidos).
    """
    api_key = os.getenv('BING_API_KEY')
    api_endpoint = os.getenv('BING_API_ENDPOINT')
    if not api_key:
        raise ValueError(
            "La clave de API de Bing no está configurada en el archivo .env")
    if not api_endpoint:
        raise ValueError(
            "El endpoint de la API de Bing no está configurado en el archivo .env")

    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
    }  # cSpell:ignore Apim
    params = {
        'mkt': region,
    }
    response = requests.get(api_endpoint, headers=headers,
                            params=params, timeout=10)
    response.raise_for_status()
    trending_searches = response.json()

    # Imprime las diez primeras tendencias de búsqueda numeradas
    for i, trend in enumerate(trending_searches['value'][:10], start=1):
        print(f"{i}. {trend['name']}")


if __name__ == "__main__":
    # Solicita al usuario que ingrese el nombre del país
    country_name = input(
        "Ingrese el nombre del país (por ejemplo, 'colombia', 'united states'): ").strip().lower()

    # Obtiene el código del país
    region_code = country_codes.get(country_name)
    if not region_code:
        print("País o región no válido.")
    else:
        # Consulta las tendencias de búsqueda en Bing para la región ingresada
        get_bing_trending_searches(region_code)
