import folium
from folium.plugins import AntPath

# Definição dos 10 principais aeroportos da América Latina
AIRPORTS = [
    {"name": "GRU - São Paulo/Guarulhos", "lat": -23.4356, "lon": -46.4731},
    {"name": "EZE - Buenos Aires/Ezeiza", "lat": -34.8222, "lon": -58.5358},
    {"name": "BOG - Bogotá/El Dorado", "lat": 4.7016, "lon": -74.1469},
    {"name": "SCL - Santiago/Arturo Merino Benítez", "lat": -33.3930, "lon": -70.7858},
    {"name": "LIM - Lima/Jorge Chávez", "lat": -12.0219, "lon": -77.1143},
    {"name": "PTY - Cidade do Panamá/Tocumen", "lat": 9.0714, "lon": -79.3835},
    {"name": "MEX - Cidade do México/B. Juárez", "lat": 19.4361, "lon": -99.0719},
    {"name": "GIG - Rio de Janeiro/Galeão", "lat": -22.8090, "lon": -43.2506},
    {"name": "CUN - Cancún International", "lat": 21.0365, "lon": -86.8771},
    {"name": "FOR - Fortaleza/Pinto Martins", "lat": -3.7763, "lon": -38.5326}
]

def plot_flight_on_map(trajectory, save_path="results/flight_map.html"):
    if len(trajectory) < 2:
        print("❌ Trajetória insuficiente para gerar mapa.")
        return

    # Ponto central do mapa
    avg_lat = sum(p[0] for p in trajectory) / len(trajectory)
    avg_lon = sum(p[1] for p in trajectory) / len(trajectory)

    # Cria mapa centrado
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=5)

    # Linha animada da trajetória
    AntPath(trajectory, color="blue", weight=4).add_to(m)

    # Marcador com ícone de avião no início
    folium.Marker(
        location=trajectory[0],
        popup="Início",
        icon=folium.DivIcon(html="<div style='font-size: 24px;'>✈️</div>")
    ).add_to(m)

    # Adiciona aeroportos alternativos
    for ap in AIRPORTS:
        folium.Marker(
            location=[ap["lat"], ap["lon"]],
            popup=ap["name"],
            icon=folium.Icon(color='green', icon='plane', prefix='fa')
        ).add_to(m)

    # Salva mapa como HTML
    m.save(save_path)
    print(f"🌍 Mapa salvo em {save_path}")
