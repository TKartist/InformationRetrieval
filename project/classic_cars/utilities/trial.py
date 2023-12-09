from indexerScript import generateIndex, getQueryResult, generateTargetFile
from clustering import perform_clustering
import json
import pandas as pd
from file_paths import DBPATH

db_objs = []
# print(DBPATH)

with open(DBPATH, "r") as f:
    objects = json.load(f)
    for obj in objects:
        db_objs.append(obj)

preIndexTable = pd.read_json(DBPATH)
index = generateIndex(preIndexTable)

query1 = [["q1", "mercedes bmw x1"]]
x = getQueryResult(index, query1, db_objs)
# print(x)
z = perform_clustering(x)
z.to_csv("clustered.csv")


# generateTargetFile()
