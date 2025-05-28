import os
import pandas as pd
import matplotlib.pyplot as plt
import umap
import numpy as np

X_series = []
y_series = []

def load_data(filepath="data/flights_sample.csv"):
    df = pd.read_csv(filepath)
    X = df[["velocity", "vertical_rate", "geo_altitude", "hour"]].values
    y = df["classe"].values
    return X, y

def plot_umap(X, y, save_path="results/plots/umap_projection.png"):
    from sklearn.impute import SimpleImputer

    # Imputação
    imputer = SimpleImputer(strategy="mean")
    X_imputed = imputer.fit_transform(X)

    mask = ~np.isnan(X_imputed).any(axis=1)
    X_clean = X_imputed[mask]
    y_clean = np.array(y)[mask]

    reducer = umap.UMAP()
    embedding = reducer.fit_transform(X_clean)

    plt.figure(figsize=(10, 7))
    scatter = plt.scatter(embedding[:, 0], embedding[:, 1], c=y_clean, cmap='Spectral', s=15)
    plt.colorbar(scatter, label='Velocidade')
    plt.title("Projeção UMAP dos dados de voo (cor = velocidade)")
    plt.xlabel("UMAP 1")
    plt.ylabel("UMAP 2")
    plt.tight_layout()
    save_path = "results/plots/umap_projection.png"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    print(f"✔️ Projeção salva em {save_path}")
    plt.show() 
    # Guarda os dados para animação
    X_series.append(X)
    y_series.append(y)

def plot_trajectory(df, save_path="results/plots/trajectory.png"):
    if "icao24" not in df.columns:
        print("❌ Dados não possuem 'icao24'.")
        return

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.figure(figsize=(10, 6))
    for aircraft in df["icao24"].unique():
        traj = df[df["icao24"] == aircraft]
        plt.plot(traj["longitude"], traj["latitude"], marker='o', label=aircraft, linewidth=1)

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Trajetórias dos aviões (latitude vs longitude)")
    plt.legend(loc="best", fontsize=6)
    plt.grid(True)
    plt.savefig(save_path)
    print(f"🗺️ Trajetória salva em {save_path}")
    plt.close()
