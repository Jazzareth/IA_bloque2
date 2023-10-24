import os
import time
import pandas as pd
import config_path
import shutil

path= config_path.path
path = os.path.join(path, "dummies_data")

dest_dir = 'D:\\Principal\\Escuela\\Actual\\TEC\\semestre7\\bloque2_IA\\reto\\f\\dummies_copy'
target_val = 'target_boolean'
# Función para verificar si un archivo debe ser renombrado
ones_f = []
def read_conteo(archivo, path=path):
    #column_name = ['time','col1_boolean','col2_boolean','col3_boolean','col4_boolean','col5_float','col6_float','col7_float','col8_float','col9_float','col10_float','col11_float','col12_float','col13_float','col14_float','col15_float','col16_float','col17_float','col18_float','col19_float','col20_float','col21_float','col22_float','col23_float','col24_float','col25_float','col26_float','col27_float','col28_float','target_boolean','target_boolean2','col31_integer','col32_integer','col33_integer','col34_integer','col35_integer','col36_integer']
    path = os.path.join(path, archivo)
    new_row = {}
    try:
        # Lee el archivo CSV en un DataFrame de Pandas
        #df = pd.read_csv(path, usecols=column_name)
        df = pd.read_csv(path)
        #print(df)
        rows = len(df[target_val])
        ones = (df[target_val] == 1).sum()
        zeros = (df[target_val] == 0).sum()
        num_columns=len(list(df.columns))
        
        #print('------')
        nNaNs = df.isna().values.sum()
        #print('nan numbers: \n',nNaNs)
        #print('------')
        # Verifica si hay al menos un 1 en la columna "Stable cruise"
        new_row['name'] = archivo
        new_row['rows'] = rows
        new_row['columns'] = num_columns
        new_row['ones'] = ones
        new_row['zeros'] = zeros
        new_row['numNaNs'] = nNaNs
        new_row['Intial_time'] = df['time'][0]
        new_row['Final_time'] = df['time'][rows-1]
        if ones > 0:
            ones_f.append(archivo)


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

print("Archivos con al menos un 1 en la columna 'Stable cruise':" + str(len(info[info['ones'] > 0])))
print("Archivos con todos 0 en la columna 'Stable cruise':" + str(len(info[info['ones'] == 0])))
print("Porcentaje de archivos con al menos un 1: "+ str(100*len(info[info['ones'] > 0])/len(info))+ "%")
print("Peso promedio de los 1: " + str(info['ones'].sum()/info['rows'].sum()))

print("Creatimg results.csv")
info.to_csv('results.csv')
print(ones_f)

for i in ones_f:
    spath = os.path.join(path, i)
    shutil.copy2(spath, dest_dir)



end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
