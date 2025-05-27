# src/preprocess.py

import pandas as pd

# ==== Pré-processamento dos dados ====
def preprocess_flight_data(df):
    df = df.dropna(subset=["latitude", "longitude", "velocity"])
    df['callsign'] = df['callsign'].astype(str).str.strip()
    df['label'] = df['callsign'].apply(lambda x: 1 if any(op in x for op in ['GOL', 'AZU', 'TAM', 'LAT']) else 0)
    return df[["icao24", "latitude", "longitude", "velocity", "baro_altitude", "label"]]