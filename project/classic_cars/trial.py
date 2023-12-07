from indexerScript import generateIndex
from indexerScript import generateTargetFile
from indexerScript import getQueryResult
import json
import pandas as pd

DBPATH = "./jsonDB.json"
INDEXPATH = "./indexJson.json"

db_objs = []

with open(DBPATH, "r") as f:
    objects = json.load(f)
    for obj in objects:
        db_objs.append(obj)

preIndexTable = pd.read_json(INDEXPATH)
index = generateIndex(preIndexTable)
query = [["q1", "mercedes x1"], ["q2", "bmw luxury car auction"]]
getQueryResult(index, query, db_objs)
query1 = [["q1", "mercedes"], ["q2", "mercedes luxury car auction"]]
getQueryResult(index, query1, db_objs)
