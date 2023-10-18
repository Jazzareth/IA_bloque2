import os
import pandas as pd

path = 'D:\\Principal\\Escuela\\Actual\\TEC\\semestre7\\bloque2_IA\\reto\\f\\diffs\\'
lf = []

for dirname, _, filenames in os.walk(path): #datos de la competencia
    for filename in filenames:
        if filename[-3:] == 'csv':
            d = os.path.join(dirname, filename)
            lf.append(filename)
            print(d)


def calcDiff(file, path, ri):
    path = os.path.join(path, file)
    try:
        # Lee el archivo CSV en un DataFrame de Pandas
        #df = pd.read_csv(path, usecols=column_name)
        df = pd.read_csv(path)

        d = df.drop(['time','col1_boolean','col2_boolean','col3_boolean','col4_boolean','target_col','target_col.1'], axis=1)
        d = d.iloc[: , 1:]
        r = d.iloc[2]

        #new_row['column'] = rows
        #new_row['diff'] = num_columns
        #ri = pd.DataFrame(columns=['file','column','diff'])
        for i in range(0,len(r),2):
            #print(r[i], ' - ',r[i+1],' = ', abs(r[i] - r[i+1]))
            cDiff = ((r[i] - r[i+1]) / r[i]) * 100
            ro = pd.DataFrame([[file,r.index[i], cDiff]], columns=['file','column','diff'])
            ri = pd.concat([ri,ro], 
                    #columns=['file','column','diff'],
                    ignore_index=True)
        return ri

    except Exception as e:
        print(f"Error al procesar el archivo {file}: {str(e)}")

df = pd.DataFrame(columns=['file','column','diff'])
for f in lf:
    df = calcDiff(f, path, df)

df.to_csv('D:\\Principal\\Escuela\\Actual\\TEC\\semestre7\\bloque2_IA\\reto\\f\\diffs\\descDiff.csv')