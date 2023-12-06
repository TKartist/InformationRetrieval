
import pyterrier as pt
import pandas as pd

json_files = ["content_scrapper_ccc.json", "file2.json", "file3.json"]

# Create an empty list to store the Python objects.
python_objects = []

# Load each JSON file into a Python object.
for json_file in json_files:
    with open(json_file, "r") as f:
        python_objects.append(json.load(f))

# Dump all the Python objects into a single JSON file.
with open("combined.json", "w") as f:
    json.dump(python_objects, f, indent=4)
x = pd.read_json('./contents_ccc.json')

print("hello")

