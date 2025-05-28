import folium
from folium.plugins import AntPath

def plot_flight_on_map(trajectory, save_path="results/flight_map.html"):
    if len(trajectory) < 2:
        print("❌ Trajetória insuficiente para gerar mapa.")
        return

    # Ponto central do mapa
    avg_lat = sum(p[0] for p in trajectory) / len(trajectory)
    avg_lon = sum(p[1] for p in trajectory) / len(trajectory)

    # Cria mapa centrado
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=10)

    # Linha animada da trajetória
    AntPath(trajectory, color="blue", weight=4).add_to(m)

    # Marcador com ícone de avião no início
    folium.Marker(
        location=trajectory[0],
        popup="Início",
        icon=folium.DivIcon(html="<div style='font-size: 24px;'>✈️</div>")
    ).add_to(m)

    # Salva mapa como HTML
    m.save(save_path)
    print(f"🌍 Mapa salvo em {save_path}")
