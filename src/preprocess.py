# src/preprocess.py

import pandas as pd
import numpy as np

def preprocess_flight_data(df):
    # Remove duplicatas com base nas coordenadas
    df = df.drop_duplicates(subset=["icao24", "latitude", "longitude"])

    # Remove registros com valores ausentes em colunas importantes
    df = df.dropna(subset=["longitude", "latitude", "velocity"])

    # Filtra velocidades válidas
    df = df[(df["velocity"] > 0)]
    df["velocity"] = df["velocity"].clip(upper=300)

    # Ordena por tempo de posição
    df = df.sort_values("time_position")

    # Seleciona a aeronave com maior número de registros distintos
    #top_aircraft = df['icao24'].value_counts().idxmax()
    #df = df[df['icao24'] == top_aircraft]

    # (Opcional) Adiciona leve jitter para evitar pontos exatamente sobrepostos
    df["latitude"] += np.random.normal(0, 0.00005, size=len(df))
    df["longitude"] += np.random.normal(0, 0.00005, size=len(df))

    return df
