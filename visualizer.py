import folium
import pandas as pd

def plot_route_on_map(route, airports_df, filename="results/route_map.html"):
    lats = [p[0] for p in route]
    lons = [p[1] for p in route]
    center = [sum(lats)/len(lats), sum(lons)/len(lons)]
    m = folium.Map(location=center, zoom_start=6)
    for _, row in airports_df.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['IATA']} - {row['Nome']}",
            icon=folium.Icon(color='blue', icon='plane', prefix='fa')
        ).add_to(m)
    folium.PolyLine(route, color="red", weight=4, opacity=0.8).add_to(m)
    for i, (lat, lon) in enumerate(route):
        folium.CircleMarker([lat, lon], radius=4, color='black', fill=True, fill_color='yellow', popup=f"WP{i}").add_to(m)
    m.save(filename)
    print(f"Mapa salvo em {filename}")

def plot_evolution_on_map(routes_per_gen, airports_df, filename="results/evolution_map.html"):
    if not routes_per_gen:
        print("Nenhuma rota para exibir.")
        return
    lats = [p[0] for p in routes_per_gen[-1]]
    lons = [p[1] for p in routes_per_gen[-1]]
    center = [sum(lats)/len(lats), sum(lons)/len(lons)]
    m = folium.Map(location=center, zoom_start=6)
    for _, row in airports_df.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['IATA']} - {row['Nome']}",
            icon=folium.Icon(color='blue', icon='plane', prefix='fa')
        ).add_to(m)
    n = len(routes_per_gen)
    for i, route in enumerate(routes_per_gen):
        color = f"#{int(255*(i/n)):02x}00{int(255*(1-i/n)):02x}"
        opacity = 0.3 + 0.7 * (i/(n-1) if n>1 else 1)
        folium.PolyLine(route, color=color, weight=2 if i<n-1 else 5, opacity=opacity).add_to(m)
    for i, (lat, lon) in enumerate(routes_per_gen[-1]):
        folium.CircleMarker([lat, lon], radius=4, color='black', fill=True, fill_color='yellow', popup=f"WP{i}").add_to(m)
    m.save(filename)
    print(f"Mapa da evolução salvo em {filename}") 