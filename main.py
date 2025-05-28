# main.py

from src.fetch_data import fetch_opensky_data
from src.preprocess import preprocess_flight_data
from src.flight_rl_env import simulate_evolutionary_navigation
from src.map_visualization import plot_flight_on_map
import os
import pandas as pd

def main():
    print("\n🔄 Baixando dados do OpenSky Network...")
    
    df_raw = fetch_opensky_data(
    lamin=-35.0,    # Latitude mínima (ex: sul da Argentina)
    lomin=-85.0,    # Longitude mínima (ex: oeste da América do Sul)
    lamax=15.0,     # Latitude máxima (ex: Caribe ou México)
    lomax=-30.0,    # Longitude máxima (litoral do Brasil)
    pages=40,
    delay=1.5
    )

    print("\n🧹 Processando dados...")
    df_proc = preprocess_flight_data(df_raw)
    print(f"Total de registros após o pré-processamento: {len(df_proc)}")
    print("📊 Colunas disponíveis:", df_proc.columns.tolist())

    os.makedirs("data", exist_ok=True)
    df_proc.to_csv("data/flights_sample.csv", index=False)
    print("✔️ Dados salvos em data/flights_sample.csv")

    print("\n🚀 Simulando navegação evolutiva...")
    simulate_evolutionary_navigation(df_proc)

    trajectory_coords = df_proc[['latitude', 'longitude']].dropna().values.tolist()
    plot_flight_on_map(trajectory_coords)

if __name__ == "__main__":
    main()
