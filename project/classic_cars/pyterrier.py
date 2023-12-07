import json
import os
import pyterrier as pt
import pandas as pd

json_files = ["contents_ccc.json", "contents_erc.json", "contents_ccs.json"]
DBPATH = "./jsonDB.json"
INDEXPATH = "./indexJson.json"

# Create an empty list to store the Python objects.
db_objects = []
index_objects = []

def convJSON2Str(jsonObj, docNo):
    make = jsonObj["make"].replace("+", " ")
    text = "make : " + make
    text += " model : " + jsonObj["model"]
    text += " year : " + jsonObj["year"]
    description = jsonObj["desc"]
    encoded = description.encode("ascii", "ignore")
    cleanDesc = encoded.decode()
    text += " description : " + cleanDesc
    text += " price : " + str(jsonObj["price"])
    return {"docno" : "d" + str(docNo), "text" : text}

def generateTargetFile():
    docno = 1
    for json_file in json_files:
        with open(json_file, "r") as f:
            objects = json.load(f)
            for obj in objects:
                db_objects.append(obj)
                index_objects.append(convJSON2Str(obj, docno))
                docno += 1
        with open(DBPATH, "w") as f:
            json.dump(db_objects, f, indent=4)
        with open(INDEXPATH, "w") as fi:
            json.dump(index_objects, fi, indent=4)

generateTargetFile()



    
