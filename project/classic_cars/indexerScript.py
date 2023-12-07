import json
import os
import pandas as pd
import pyterrier as pt

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
    cleanDesc = (encoded.decode()).replace("\n", " ")
    text += " description : " + cleanDesc
    text += " price : " + str(jsonObj["price"])
    return {"docno": "d" + str(docNo), "text": text}


def generateTargetFile():
    docno = 1
    for json_file in json_files:
        with open(json_file, "r") as f:
            objects = json.load(f)
            for obj in objects:
                index_objects.append(convJSON2Str(obj, docno))
                obj["docno"] = "d" + str(docno)
                db_objects.append(obj)
                docno += 1
        with open(DBPATH, "w") as f:
            json.dump(db_objects, f, indent=4)
        with open(INDEXPATH, "w") as fi:
            json.dump(index_objects, fi, indent=4)


if os.path.isfile(DBPATH) == False or os.path.isfile(INDEXPATH) == False:
    generateTargetFile()

# Moving the JSON to Dataframe
preIndexTable = pd.read_json(INDEXPATH)

# Initializing pyterrier
if not pt.started():
    pt.init()

indexer = pt.DFIndexer("./index_classic_cars", overwrite=True)

index_ref = indexer.index(preIndexTable["text"], preIndexTable["docno"])
index_ref.toString()

index = pt.IndexFactory.of(index_ref)

# print(index.getCollectionStatistics().toString())

# for kv in index.getLexicon():
#     print(kv.getKey())
#     print(index.getLexicon()[kv.getKey()].toString())
#     print("******************************************")

# word_ = "x1"
# pointer = index.getLexicon()[word_]
# for posting in index.getInvertedIndex().getPostings(pointer):
#     print(posting.toString() + "doclen=%d" % posting.getDocumentLength())


def retrieve_car_info(cdf):
    car_make = []
    car_brand = []
    for i in range(cdf.shape[0]):
        db_objects


bm25 = pt.BatchRetrieve(index, num_results=10, wmodel="BM25")
queries = pd.DataFrame(
    [["q1", "mercedes x1"], ["q2", "bmw luxury car auction"]],
    columns=["qid", "query"],
)
results = bm25.transform(queries)

pt.io.write_results(results, "res_bm25.txt", format="trec")
