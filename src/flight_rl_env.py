import matplotlib.pyplot as plt
import os

def simulate_evolutionary_navigation(df):
    print("[simulação fictícia] Ambiente de simulação de voo iniciado...")

    if df.empty:
        print("❌ Nenhum dado disponível para simulação.")
        return

    print(df[["latitude", "longitude", "velocity"]].head())

    os.makedirs("results", exist_ok=True)

    plt.figure(figsize=(8, 6))
    plt.plot(df["longitude"], df["latitude"], marker='o', linestyle='-')
    plt.title("Trajetória de voo simulada")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.savefig("results/trajectory.png")
    print("📍 Trajetória salva em results/trajectory.png")
