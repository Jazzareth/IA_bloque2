import os
import time
import pandas as pd
import config_path


path= config_path.path
path = os.path.join(path, "dummies_data")
# Función para verificar si un archivo debe ser renombrado

def read_conteo(archivo, path=path):
    column_name = ["target_boolean","time"]
    path = os.path.join(path, archivo)
    new_row = {}
    try:
        # Lee el archivo CSV en un DataFrame de Pandas
        df = pd.read_csv(path)
        num_columns=len(list(df.columns))
        df = df[column_name]
        rows = len(df[column_name[0]])
        ones = (df[column_name[0]] == 1).sum()
        zeros = (df[column_name[0]] == 0).sum()
        # Verifica si hay al menos un 1 en la columna "Stable cruise"
        new_row['name'] = archivo
        new_row['rows'] = rows
        new_row['ones'] = ones
        new_row['zeros'] = zeros
        new_row['Intial_time'] = df['time'][0]
        new_row['Final_time'] = df['time'][rows-1]
        new_row['columns'] = num_columns
        return new_row
    except Exception as e:
        print(f"Error al procesar el archivo {archivo}: {str(e)}")
        
    return {}


# Itera sobre los archivos en el directorio
archivos = os.listdir(path)
info = pd.DataFrame(columns=['name', 'rows', 'ones', 'zeros'])
fails=0;

start_time = time.time()
for archivo in archivos:
    new_row = read_conteo(archivo)
    #print(new_row)
    if new_row:
        new_row_df = pd.DataFrame([new_row])
        info = pd.concat([info, new_row_df], ignore_index=True)
    else:
        fails+=1

print ("Fails in read: "+str(fails))
print(info)
#Weight avarage of ones
info['ones'] = info['ones'].astype(float)
info['rows'] = info['rows'].astype(float)
info['weightOnes'] = info['ones']/info['rows']

print("Archivos con al menos un 1 en la columna 'Stable':" + str(len(info[info['ones'] > 0])))
print("Archivos con todos 0 en la columna 'Stable':" + str(len(info[info['ones'] == 0])))
print("Porcentaje de archivos con al menos un 1: "+ str(100*len(info[info['ones'] > 0])/len(info))+ "%")
print("Peso promedio de los 1: " + str(info['ones'].sum()/info['rows'].sum()))

print("Creatimg results.csv")
info.to_csv('results.csv')

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
