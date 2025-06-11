# 🛩️ OpenSky Neuroevo

**Flight trajectory simulation and visualization using neuroevolutionary algorithms and real-world data.**

This project leverages live or historical flight data from the OpenSky Network to simulate and evolve neural networks capable of learning navigation behavior. It focuses on trajectory analysis and the use of evolutionary algorithms to explore air traffic patterns in Latin America.

---

## 🎯 Goals

- Collect and process live or historical flight data from the OpenSky Network.
- Filter relevant flight trajectories for simulation.
- Train evolved neural networks (NEAT) to mimic or optimize navigation behavior.
- Visualize real flight paths and alternative landing options using interactive maps.
- Improve the interpretability of AI by analyzing decision paths and flight routes.

---

## 🧠 Tech Stack

- `Python 3.11+`
- [`neat-python`](https://github.com/CodeReclaimers/neat-python) — NeuroEvolution of Augmenting Topologies
- `pandas`, `numpy`, `matplotlib` — data wrangling and visualization
- `folium` — interactive flight map rendering
- OpenSky Network API (live ADS-B/Mode-S data)

---

## 🗺️ Example Output

Example output is saved to a `results/` directory when you run the
simulations. The interactive map `flight_map.html` will be generated there.

---

## 📁 Project Structure

```

opensky-neuroevo/
├── data/              # Sample datasets
├── app.py             # Streamlit interface
├── evolution.py       # Genetic algorithm
├── main.py            # CLI interface
├── synthetic_data.py  # Data generation utilities
├── visualizer.py      # Map plotting functions
├── requirements.txt
└── README.md

```

---

## 🚀 Getting Started

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Launch the interactive explorer (Streamlit):

```bash
streamlit run app.py
# or
python main.py --ui
```


---

## 🛬 Airports Configuration

The system considers the **top 10 major airports in Latin America** as possible emergency landing or redirection options during trajectory simulation.

---

## 📚 Academic Context

This repository supports a Master’s research project at **UFRGS** (Federal University of Rio Grande do Sul), under the supervision of **Prof. Dr. Bruno Iochins Grisci**.

---

## 🚧 Status

In active development — contributions and academic collaborations are welcome!

---

## 📄 License

[MIT License](LICENSE)
