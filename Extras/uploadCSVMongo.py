from pymongo import MongoClient
import numpy as np
import pandas as pd
import json
import os
import csv 

columns = []

def get_db_handle(db_name):

    client = MongoClient("mongodb://localhost:27017")

    db = client[db_name]
    #db = MongoClient[db_name]
                     
    return db

def dumpCSV(dir,fname,col):
    header = columns
    csvFile = open(dir, 'r')
    #csvFile = open('csvs/stores.csv', 'r')
    reader = csv.DictReader(csvFile)
    c=0
    for each in reader:
        row = {}
        for field in header:
            row[field] = each[field]
        row['fname'] = fname
        col.insert_one(row)
    csvFile.close()
    pass

db = get_db_handle("dumpCSV")
print(db)
testCol = db['test']
print(testCol)
for dirname, _, filenames in os.walk('csvs'): #datos de la competencia
    for filename in filenames:
        #print(os.path.join(dirname, filename))
        print(filename[:-4])
        dumpCSV(os.path.join(dirname, filename),filename[:-4],testCol)
