import os
import pandas as pd
import config_path
import concurrent.futures
import random
import matplotlib.pyplot as plt

path = config_path.path
path = os.path.join(path, "dummies_data")

def read_conteo(archivo, path=path):
    column_name = ["target_boolean", "time", "col"] # Agregado col5_float
    path = os.path.join(path, archivo)
    new_row = {}
    try:
        df = pd.read_csv(path, usecols=column_name)
        rows = len(df[column_name[0]])
        ones = (df[column_name[0]] == 1).sum()
        zeros = (df[column_name[0]] == 0).sum()
        new_row['name'] = archivo
        new_row['rows'] = rows
        new_row['ones'] = ones
        new_row['zeros'] = zeros
        new_row['Intial_time'] = df['time'][0]
        new_row['Final_time'] = df['time'][rows-1]
        return new_row
    except Exception as e:
        print(f"Error al procesar el archivo {archivo}: {str(e)}")
    return {}

archivos = os.listdir(path)
info = pd.DataFrame(columns=['name', 'rows', 'ones', 'zeros'])

start_time = time.time()

num_threads = 6
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    results = [executor.submit(read_conteo, archivo) for archivo in archivos]
    for f in concurrent.futures.as_completed(results):
        new_row = f.result()
        if new_row:
            new_row_df = pd.DataFrame([new_row])
            info = pd.concat([info, new_row_df], ignore_index=True)

# Filtrar archivos con más de un "1"
files_with_ones = info[info['ones'] > 1]

# Elegir 5 archivos aleatorios
selected_files = files_with_ones.sample(n=5)['name'].tolist()

# Graficar los datos de los archivos seleccionados
for file in selected_files:
    df = pd.read_csv(os.path.join(path, file), usecols=["time", "col"])
    plt.plot(df["time"], df["colt"], label=file)

plt.legend()
plt.xlabel('Time')
plt.ylabel('Alt (assuming col)')
plt.title('Time vs Altitude for 5 Random Files')
plt.show()
