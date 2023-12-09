from indexerScript import generateIndex, getQueryResult, generateTargetFile
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
query = [["q1", "mercedes x1"], ["q2", "bmw luxury car auction"]]
x = getQueryResult(index, query, db_objs)
x.to_csv("clustered.csv", index=False, encoding="utf-8")

query1 = [["q1", "mercedes"], ["q2", "mercedes luxury car auction"]]
x = getQueryResult(index, query1, db_objs)
x.to_csv("clustered2.csv")

# generateTargetFile()
