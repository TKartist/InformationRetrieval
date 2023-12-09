import json
import os
import pandas as pd
import pyterrier as pt
import re
from file_paths import DBPATH, INDEXPATH, json_files

# Create an empty list to store the Python objects.


def convJSON2Str(jsonObj, docNo):
    make = jsonObj["make"].replace("+", " ")
    text = "make : " + make
    text += " model : " + jsonObj["model"]
    text += " year : " + jsonObj["year"]
    description = jsonObj["desc"]
    encoded = description.encode("ascii", "ignore")
    cleanDesc = (encoded.decode()).replace("\n", " ")
    text += " description : " + cleanDesc
    text += " price : " + str(jsonObj["price"])
    return {"docno": "d" + str(docNo), "text": text}


def alterObject(obj, docno):
    newObj = {}
    newObj["docno"] = "d" + str(docno)
    if obj["price"]:
        copyPrice = obj["price"]
        valPrice = (copyPrice.split(" ")[0])[1:]
        numPrice = valPrice.replace(",", "")
        if numPrice.isdigit():
            newObj["price"] = int(numPrice)
        else:
            newObj["price"] = 0
    else:
        newObj["price"] = 0
    brand = obj["make"].replace("+", " ")
    newObj["brand"] = brand
    newObj["model"] = obj["model"]
    newObj["year"] = obj["year"]
    newObj["description"] = obj["desc"]
    newObj["image_url"] = obj["image"]
    newObj["detail_url"] = obj["link"]
    return newObj


def generateTargetFile():
    db_objects = []
    index_objects = []
    docno = 1
    for json_file in json_files:
        with open(json_file, "r") as f:
            objects = json.load(f)
            for obj in objects:
                index_objects.append(convJSON2Str(obj, docno))
                newObj = alterObject(obj, docno)
                db_objects.append(newObj)
                docno += 1
        with open(DBPATH, "w") as f:
            json.dump(db_objects, f, indent=4)
        with open(INDEXPATH, "w") as fi:
            json.dump(index_objects, fi, indent=4)


def generateIndex(preIndexTable):
    if not pt.started():
        pt.init()

    indexer = pt.DFIndexer("./index_classic_cars", overwrite=True)

    index_ref = indexer.index(preIndexTable["text"], preIndexTable["docno"])
    index_ref.toString()
    index = pt.IndexFactory.of(index_ref)
    return index


# print(index.getCollectionStatistics().toString())

# for kv in index.getLexicon():
#     print(kv.getKey())
#     print(index.getLexicon()[kv.getKey()].toString())
#     print("******************************************")

# word_ = "x1"
# pointer = index.getLexicon()[word_]
# for posting in index.getInvertedIndex().getPostings(pointer):
#     print(posting.toString() + "doclen=%d" % posting.getDocumentLength())


def retrieve_car_info(cdf, db_objects):
    car_make = []
    car_model = []
    for i in range(cdf.shape[0]):
        docId = cdf.loc[i, "docno"]
        docNo = int(docId[1:]) - 1
        car_make.append(db_objects[docNo]["make"])
        car_model.append(db_objects[docNo]["model"])
    cdf["make"] = car_make
    cdf["model"] = car_model
    return cdf


def getQueryResult(index, query, db_objs):
    bm25 = pt.BatchRetrieve(index, num_results=10, wmodel="BM25")

    queries = pd.DataFrame(
        query,
        columns=["qid", "query"],
    )
    results = bm25.transform(queries)
    formatedResult = retrieve_car_info(results, db_objs)
    print(formatedResult)  # For now just printing the query result
