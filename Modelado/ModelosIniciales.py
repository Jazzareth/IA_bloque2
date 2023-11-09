import os
import time
import numpy as np
import pandas as pd
import dask
import dask.dataframe as dd
import shutil
import dask.array as da
import dask_ml as dml
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
import joblib
from dask_ml.model_selection import GridSearchCV
from sklearn.metrics import precision_score, recall_score
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay

from sklearn.ensemble import RandomForestClassifier
path='input_final_path'
p1=path+'\\f1.csv'
p2=path+'\\f2.csv'
l=[p1,p2]

from dask.distributed import Client
client = Client(n_workers=3, processes=True)
client

ddf = dd.read_csv(l)
ddf = ddf.drop(['Unnamed: 0','col31_integer','col33_integer','col35_integer', 'Fname', 'addedVar1','addedVar2','addedVar3'],axis=1)
ddf.head(5)

train, test = dml.model_selection.train_test_split(ddf, train_size=0.8,test_size=0.2,random_state=0)
train.head(5)

train_x = train[['time', 'col5_float', 'col7_float','col9_float','col11_float','col13_float',
                'col15_float', 'col7_float', 'col19_float', 'col21_float',
                'col23_float', 'col25_float', 'col27_float']]
train_y = train['target_boolean']
test_x = test[['time', 'col5_float', 'col7_float','col9_float','col11_float','col13_float',
                'col15_float', 'col7_float', 'col19_float', 'col21_float',
                'col23_float', 'col25_float', 'col27_float']]
test_y = test['target_boolean']


valPath = 'validationDataPath'
valDF = dd.read_csv(valPath+'*.csv')
valX = valDF[['time', 'col5_float', 'col7_float','col9_float','col11_float','col13_float',
                'col15_float', 'col7_float', 'col19_float', 'col21_float',
                'col23_float', 'col25_float', 'col27_float']]
valY = valDF[['target_boolean']]

print('--------------Modelo 1-----------------')

with joblib.parallel_backend('dask'):
    randFor1 = RandomForestClassifier(n_estimators=4, n_jobs=4)
    randFor1.fit(train_x,train_y)

y_preds = randFor1.predict(test_x)
accuracy = accuracy_score(test_y, y_preds)
print("Test Accuracy:", accuracy)

y_predVals = randFor1.predict(valX)
accuracy = accuracy_score(valY, y_predVals)
print("Val Accuracy:", accuracy)

y_preds = randFor1.predict(test_x)

precision = precision_score(test_y, y_preds)
recall = recall_score(test_y, y_preds)

print("Test Precision:", precision)

print("Test Recall:", recall)

f1_score = 2 * (precision * recall) / (precision + recall)
print("Test F1-Score:", f1_score)

val_precision = precision_score(valY, y_predVals)
val_recall = recall_score(valY, y_predVals)
print("Val Precision:", val_precision)
print("Val Recall:", val_recall)
val_f1_score = 2 * (val_precision * val_recall) / (val_precision + val_recall)
print("Val F1-Score:", val_f1_score)
cm=metrics.confusion_matrix(valY, y_predVals)
disp=ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.show()

print(cm)



print('--------------Modelo 2-----------------')


params = {'n_estimators':np.random.randint(50,100,size=10),
         'max_depth':np.random.randint(1,20,size=5),
          'criterion':['gini','entropy'],
          'bootstrap':[True]
         }
scor = ['accuracy','f1','precision','recall']
grid_search = GridSearchCV(RandomForestClassifier(),params, cv=3, scoring=scor, refit='f1', n_jobs=-1)
grid_search.fit(train_x,train_y)

print(grid_search.best_estimator_)

gsScore = grid_search.scorer_

print(gsScore['accuracy'])

print(grid_search.best_score_)

bestFor = RandomForestClassifier(criterion='entropy', max_depth=7, n_estimators=65)
with joblib.parallel_backend('dask'):
    bestFor.fit(train_x,train_y)
bestFor



y_preds = bestFor.predict(test_x)
accuracy = accuracy_score(test_y, y_preds)
print("Test Accuracy:", accuracy)

y_predVals = bestFor.predict(valX)
accuracy = accuracy_score(valY, y_predVals)
print("Val Accuracy:", accuracy)



y_preds = bestFor.predict(test_x)

precision = precision_score(test_y, y_preds)
recall = recall_score(test_y, y_preds)

print("Test Precision:", precision)

print("Test Recall:", recall)

f1_score = 2 * (precision * recall) / (precision + recall)

print("Test F1-Score:", f1_score)

val_precision = precision_score(valY, y_predVals)
val_recall = recall_score(valY, y_predVals)

print("Val Precision:", val_precision)

print("Val Recall:", val_recall)

val_f1_score = 2 * (val_precision * val_recall) / (val_precision + val_recall)

print("Val F1-Score:", val_f1_score)


cm=metrics.confusion_matrix(valY, y_predVals)


disp=ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.show()

print(cm)




      

