# src/fetch_data.py

import pandas as pd
import requests
import time

def fetch_opensky_data(lamin, lomin, lamax, lomax, pages=5, delay=1.0):
    """
    Busca múltiplos lotes de dados do OpenSky Network.
    - pages: número de requisições consecutivas
    - delay: tempo entre as requisições (em segundos)
    """
    all_data = []

    for i in range(pages):
        print(f"Requisição {i+1}/{pages}...")
        url = f"https://opensky-network.org/api/states/all?lamin={lamin}&lomin={lomin}&lamax={lamax}&lomax={lomax}"
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                data = resp.json()
                if 'states' in data and data['states']:
                    df = pd.DataFrame(data['states'], columns=[
                        "icao24", "callsign", "origin_country", "time_position", "last_contact",
                        "longitude", "latitude", "baro_altitude", "on_ground", "velocity",
                        "true_track", "vertical_rate", "sensors", "geo_altitude", "squawk",
                        "spi", "position_source"
                    ])
                    all_data.append(df)
        except Exception as e:
            print(f"Erro na requisição: {e}")
        time.sleep(delay)

    if not all_data:
        raise Exception("Nenhum dado retornado da API")

    df_full = pd.concat(all_data, ignore_index=True)
    print(f"Total de registros coletados: {len(df_full)}")
    return df_full