# main.py

from src.fetch_data import fetch_opensky_data
from src.preprocess import preprocess_flight_data
from src.neat_train import run_neat
from src.visualize import plot_umap, load_data
import os
import pandas as pd


def main():
    print("\n🔄 Baixando dados do OpenSky Network...")
    df_raw = fetch_opensky_data(-23.7, -46.8, -23.3, -46.3)  # São Paulo

    print("\n🧹 Processando dados...")
    df_proc = preprocess_flight_data(df_raw)
    os.makedirs("data", exist_ok=True)
    df_proc.to_csv("data/flights_sample.csv", index=False)
    print("✔️ Dados salvos em data/flights_sample.csv")

    print("\n🧠 Treinando com NEAT...")
    config_path = os.path.join("config", "neat-config.txt")
    run_neat(config_path)

    print("\n🖼️ Gerando visualização UMAP...")
    X, y = load_data()
    plot_umap(X, y)


if __name__ == "__main__":
    main()
