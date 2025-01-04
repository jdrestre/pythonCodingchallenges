"""
Este script obtiene las tendencias de búsqueda actuales para una región específica. Utiliza el motor de búsqueda de Google Trends para obtener las tendencias de búsqueda actuales para una región específica. Para ello, se utiliza la biblioteca pytrends, que proporciona una interfaz para interactuar con la API de Google Trends. El script solicita al usuario que ingrese el nombre del país o región para la cual desea obtener las tendencias de búsqueda. Luego, utiliza la función trending_searches de la clase TrendReq de pytrends para obtener las tendencias de búsqueda actuales para la región especificada. Finalmente, imprime las diez primeras tendencias de búsqueda numeradas.
""" # pylint: disable=line-too-long # cSpell:ignore pytrends

from pytrends.request import TrendReq


def get_trending_searches_by_region(region):
    """
    Obtiene las tendencias de búsqueda actuales para una región específica.

    Parámetros:
    region (str): Nombre del país o región (por ejemplo, 'colombia' para Colombia, 'united_states' para Estados Unidos).
    """
    # Inicializa la solicitud de tendencias
    pytrends = TrendReq(hl='en-US', tz=360)

    # Obtiene las tendencias de búsqueda actuales para la región especificada
    trending_searches_df = pytrends.trending_searches(pn=region)

    # Selecciona las primeras diez tendencias
    top_10_trending_searches = trending_searches_df.head(10)

    # Imprime las diez primeras tendencias de búsqueda numeradas
    for i, trend in enumerate(top_10_trending_searches[0].tolist(), start=1):
        print(f"{i}. {trend}")


if __name__ == "__main__":
    # Solicita al usuario que ingrese el nombre del país
    region_ = input(
        "Ingrese el nombre del país o región (por ejemplo, 'colombia', 'united_states'): ").strip().lower()

    # Consulta las tendencias de búsqueda para la región ingresada
    get_trending_searches_by_region(region_)
