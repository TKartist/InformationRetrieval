import json
import re
import pandas as pd
import pyterrier as pt

# Contains the file paths in case of running through the JSONS
from file_paths import DBPATH, json_files


# Generates text columns of DF
def convJSON2Str(jsonObj):
    # Personalized
    make = jsonObj["make"].replace("+", " ")
    text = make
    text += " " + jsonObj["model"]
    text += " " + jsonObj["year"]
    if jsonObj["price"]:
        text += " " + jsonObj["price"]
    else:
        text += " sold vehicle"
    description = " " + jsonObj["desc"]
    encoded = description.encode("ascii", "ignore")
    cleanDesc = (encoded.decode()).replace("\n", " ")
    text += " " + cleanDesc
    text += " " + str(jsonObj["price"])
    text = re.sub(r"\(.*?\)", "", text)
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"\\", "", text)
    text = re.sub(r"-", "", text)
    text = re.sub(r"\n", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# Alters original scrapped object into a format we need
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
    newObj["text"] = convJSON2Str(obj)
    newObj["image_url"] = obj["image"]
    newObj["detail_url"] = obj["link"]
    return newObj


# Creates jsonDB file filled with all the scrapped and altered info
def generateTargetFile():
    db_objects = []
    docno = 1
    for json_file in json_files:
        with open(json_file, "r") as f:
            objects = json.load(f)
            for obj in objects:
                newObj = alterObject(obj, docno)
                db_objects.append(newObj)
                docno += 1
    with open(DBPATH, "w") as f:
        json.dump(db_objects, f, indent=4)


def generateIndex(preIndexTable):
    if not pt.started():
        pt.init()

    indexer = pt.DFIndexer("./index_classic_cars", overwrite=True)

    index_ref = indexer.index(preIndexTable["text"], preIndexTable["docno"])
    index_ref.toString()
    index = pt.IndexFactory.of(index_ref)
    bm25 = pt.BatchRetrieve(index, num_results=20, wmodel="BM25")
    return bm25


# Creates a simplified ver. of objects for clustering and display
def retrieve_car_info(cdf, db_objects):
    car_make = []
    car_model = []
    texts = []
    for i in range(cdf.shape[0]):
        docId = cdf.loc[i, "docno"]
        docNo = int(docId[1:]) - 1
        car_make.append(db_objects[docNo]["brand"])
        car_model.append(db_objects[docNo]["model"])
        texts.append(db_objects[docNo]["text"])
    cdf["brand"] = car_make
    cdf["model"] = car_model
    cdf["text"] = texts
    return cdf


def getQueryResult(bm25, query, db_objs):
    print(bm25)
    print("...Starting the Querying...")
    q = []
    q.append(query)
    qid = []
    qid.append("q1")
    queries = pd.DataFrame()
    queries["qid"] = qid
    queries["query"] = q
    print(queries)
    results = bm25.transform(queries)
    formatedResult = retrieve_car_info(results, db_objs)
    # print(formatedResult)  # For now just printing the query result
    print("...Received Query Results...")
    return formatedResult
