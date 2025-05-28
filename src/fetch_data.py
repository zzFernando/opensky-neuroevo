# src/fetch_data.py

import requests
import pandas as pd
import time
import json

with open("config/credentials.json") as f:
    creds = json.load(f)

CLIENT_ID = creds["clientId"]
CLIENT_SECRET = creds["clientSecret"]
TOKEN_URL = "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
API_URL = "https://opensky-network.org/api/states/all"

def get_access_token():
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    resp = requests.post(TOKEN_URL, data=data)
    resp.raise_for_status()
    return resp.json()["access_token"]

def fetch_opensky_data(lamin, lomin, lamax, lomax, pages=50, delay=1.0):
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}

    all_data = []
    for i in range(pages):
        print(f"Requisição {i+1}/{pages}...")
        url = f"{API_URL}?lamin={lamin}&lomin={lomin}&lamax={lamax}&lomax={lomax}"
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            if 'states' in data and data['states']:
                df = pd.DataFrame(data['states'], columns=[
                    "icao24", "callsign", "origin_country", "time_position", "last_contact",
                    "longitude", "latitude", "baro_altitude", "on_ground", "velocity",
                    "true_track", "vertical_rate", "sensors", "geo_altitude", "squawk",
                    "spi", "position_source"])
                all_data.append(df)
        time.sleep(delay)

    if not all_data:
        raise Exception("Nenhum dado retornado da API")

    return pd.concat(all_data, ignore_index=True)
