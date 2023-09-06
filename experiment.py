import os
import sys
import subprocess
import pandas as pd
from tqdm import tqdm

dataframes = []

# Quantidade de experimentos
experiments = 100

# Realizando experimentos
for i in tqdm(range(experiments)):
    subprocess.run(["python3", "main.py", "/dev/null"])
    os.rename("data/metrics.csv", f"data/metrics_{i}.csv")

# Carregando dataframes
for i in tqdm(range(experiments)):
    try:
        df = pd.read_csv(f"data/metrics_{i}.csv")
        df["experiment"] = i
        dataframes.append(df)
    except:
        print("Nenhum experimento foi excutado")
        sys.exit(0)

# Calculando média
df = pd.concat(dataframes)
print(df.groupby("network").agg({"THROUGHPUT": "mean"}))
