import pandas as pd
import numpy as np
import os

#Colocar el path de la carpeta con los archivos a analizar
path='/content/sample_data/'
contenido = os.listdir(path)

#DataFrame para unir los csv en uno solo con una columna con el nombre de cada archivo para distingirlos y clasificarlos 
df=pd.DataFrame()
for i in contenido:
  df1 = pd.read_csv(path+i)
  index=np.full(len(df1['longitude']),i)
  df1["archivo"]=index
  frames=[df,df1]
  df = pd.concat(frames)


#DataFrame para guardar las cariables de estadistica descriptiva de todas las columnas 
columns_names = df.columns.values
df_res=pd.DataFrame()
for i in columns_names:
  res=pd.DataFrame(df[i].describe())
  df_res = pd.concat([df_res, res], axis=1)

print(df_res)
#Exportar los archivos como csv 
'''df_res.to_csv("var_estadistica.csv")
df.to_csv("archivos_union.csv")'''