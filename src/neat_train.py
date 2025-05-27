import pandas as pd
import neat
import os
import pickle

# ==== Carregar dados ====
def load_data(csv_path="data/flights_sample.csv"):
    df = pd.read_csv(csv_path)
    X = df[["latitude", "longitude", "velocity", "baro_altitude"]].values
    y = df["label"].values
    return X, y

# ==== Avaliação dos genomas ====
def eval_genomes(genomes, config):
    X, y = load_data()
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        correct = 0
        for i, xi in enumerate(X):
            output = net.activate(xi)
            prediction = 1 if output[0] > 0.5 else 0
            if prediction == y[i]:
                correct += 1
        genome.fitness = correct / len(y)

# ==== Função principal de treino ====
def run_neat(config_file):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file
    )

    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    winner = pop.run(eval_genomes, 50)

    # salvar melhor rede
    with open("results/winner.pkl", "wb") as f:
        pickle.dump(winner, f)
    print("Melhor rede salva em results/winner.pkl")

# ==== Executar se chamado diretamente ====
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "..", "config", "neat-config.txt")
    run_neat(config_path)