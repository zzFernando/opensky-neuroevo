import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import umap

def load_data(csv_path="data/flights_sample.csv"):
    df = pd.read_csv(csv_path)
    X = df[["latitude", "longitude", "velocity", "baro_altitude"]].values
    y = df["label"].values
    return X, y

def plot_umap(X, y, save_path="results/plots/umap_projection.png"):
    from sklearn.impute import SimpleImputer

    # Imputa valores ausentes em X e alinha y
    imputer = SimpleImputer(strategy="mean")
    X_imputed = imputer.fit_transform(X)

    mask = ~np.isnan(X_imputed).any(axis=1)
    X_clean = X_imputed[mask]
    y_clean = np.array(y)[mask]

    reducer = umap.UMAP()
    embedding = reducer.fit_transform(X_clean)

    plt.figure(figsize=(10, 7))
    scatter = plt.scatter(embedding[:, 0], embedding[:, 1], c=y_clean, cmap='Spectral', s=15)
    plt.colorbar(scatter, label='Classe')
    plt.title("Projeção UMAP dos dados de voo")
    plt.xlabel("UMAP 1")
    plt.ylabel("UMAP 2")
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"✔️ Projeção salva em {save_path}")
    plt.show()