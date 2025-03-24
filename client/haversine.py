from math import radians, cos, sin, sqrt, atan2

def calcular_distancia(lat1, lon1, lat2, lon2):
    """
    Calcula a distância entre dois pontos geográficos usando a fórmula de Haversine.
    Retorna a distância em quilômetros.
    """
    raio_terra = 6371.0  # Raio médio da Terra em km

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return raio_terra * c
