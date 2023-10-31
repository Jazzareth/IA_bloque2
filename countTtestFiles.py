import os
import pandas as pd
import numpy as np
import itertools

p = ''
filnameCol = ''
df = pd.read_csv(p)
cols = list(df.columns)
df=df.set_index([filnameCol])

filist = []
for i in cols[1:]:
    l = list(df[(df[i]>0.05)].index)
    filist.append(l)


merged = list(itertools.chain.from_iterable(filist))
fileSet = set(merged)
print(fileSet)