import pyterrier as pt
import pandas as pd
import json

import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

nltk.download("punkt")
import string

import sklearn
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans, DBSCAN
from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import StandardScaler


if not pt.started():
    pt.init()

dataframes1 = []
dataframes2 = []
dataframes3 = []

with open("./data/result1.jsonl", "r") as file:
    for line in file:
        json_obj = json.loads(line)
        df = pd.DataFrame([json_obj])
        dataframes1.append(df)


df1 = pd.concat(dataframes1, ignore_index=True)

with open("./data/result2.jsonl", "r") as file:
    for line in file:
        json_obj = json.loads(line)
        df = pd.DataFrame([json_obj])
        dataframes2.append(df)


df2 = pd.concat(dataframes2, ignore_index=True)


with open("./data/result3.jsonl", "r") as file:
    for line in file:
        json_obj = json.loads(line)
        df = pd.DataFrame([json_obj])
        dataframes3.append(df)


df3 = pd.concat(dataframes3, ignore_index=True)

df = pd.concat([df1, df2, df3], ignore_index=True)


df["genres_concatenated"] = df["genre"].apply(lambda x: ", ".join(x))

df["text"] = df["album"] + " " + df["artist"] + " " + df["genres_concatenated"]
df["text"] = df["text"].str.lower().str.replace(r"\s+", " ", regex=True)

df["docno"] = "d" + df.index.astype(str)

df_complete = df


df = df[["docno", "text"]]

df.to_csv("./docs1.csv", index=False)

indexer = pt.DFIndexer("./index_3docs", overwrite=True)
index_ref = indexer.index(df["text"], df["docno"])
index_ref.toString()

index = pt.IndexFactory.of(index_ref)

# lets see what type index is.
type(index)

# print(index.getCollectionStatistics().toString())

# for kv in index.getLexicon():
#     print("%s  -> %s " % (kv.getKey(), " ".join(kv.getValue().toString().split())))


"""INVERTED INDEX"""

# word_ = "javelin"
# pointer = index.getLexicon()[word_]
# for posting in index.getInvertedIndex().getPostings(pointer):
#     print(posting.toString() + " doclen=%d" % posting.getDocumentLength())

# br = pt.BatchRetrieve(index, wmodel="BM25")
# br.search("javelin")

# br.search("Tender")

# br.search("Golden Apples of the Sun")

# bm25 = pt.BatchRetrieve(index, wmodel="BM25")

# bm25.search("Blonde Redhead")


def get_album(docid):
    id = int(docid[1:])
    return album_name[id]


def retriever_album(df):
    album = []
    for i in range(df.shape[0]):
        docid = df.loc[i, "docno"]
        album.append(get_album(docid))
    df["Album"] = album
    return df


def get_artist(docid):
    id = int(docid[1:])
    return artist_name[id]


def get_genres(docid):
    id = int(docid[1:])
    return generes_type[id]


def retriever_genre(df):
    genre = []
    for i in range(df.shape[0]):
        docid = df.loc[i, "docno"]
        genre.append(get_album(docid))
    df["Genre"] = genre
    return df


def get_description(docid):
    id = int(docid[1:])
    return description[id]


def get_link(docid):
    id = int(docid[1:])
    return link[id]


def get_link_img(docid):
    id = int(docid[1:])
    return img[id]


def retriever_artist(df):
    artist = []
    for i in range(df.shape[0]):
        docid = df.loc[i, "docno"]
        artist.append(get_artist(docid))
    df["Artist"] = artist
    return df


def retrieve_query(query):
    # Assuming index, pt, get_artist, get_album, get_genres, and get_description are defined/imported
    bm25 = pt.BatchRetrieve(index, wmodel="BM25")
    queries = pd.DataFrame([["q1", query]], columns=["qid", "query"])
    results = bm25.transform(queries)

    artist = []
    album = []
    genres = []
    description = []
    link = []
    image = []

    for i in range(results.shape[0]):
        docid = results.loc[i, "docno"]
        artist.append(get_artist(docid))
        album.append(get_album(docid))
        genres.append(get_genres(docid))
        description.append(get_description(docid))
        link.append(get_link(docid))
        image.append(get_link_img(docid))
    results["Artist"] = artist
    results["Album"] = album
    results["Genres"] = genres
    results["Description"] = description
    results["Link"] = link
    results["Img"] = image
    df_result = pd.DataFrame()
    df_result = results[["Artist", "Album", "Genres", "Description", "Link", "Img"]]
    print(df_result[["Artist", "Album"]])
    return df_result


def apply_stem(text, stemmer):
    # Check if the text is a string or bytes-like object
    if isinstance(text, (str, bytes)):
        words = word_tokenize(text)
        stemmed_text = " ".join([stemmer.stem(word) for word in words])
        return stemmed_text
    else:
        return ""


# Rest of your code remains unchanged
genres = df_complete["genres_concatenated"].unique()
list_genres = list(genres)
number_of_clusters = len(list_genres)
words = df["text"].values

stemmer = PorterStemmer()
df_complete["text_stemmed"] = df_complete["text"].apply(
    lambda x: apply_stem(x, stemmer)
)

# Vectorization
vectorizer = TfidfVectorizer(
    stop_words="english", lowercase=True, max_df=0.9, min_df=0.01, max_features=1000
)
X = vectorizer.fit_transform(df_complete["text_stemmed"])

# KMeans clustering
number_of_clusters = len(df_complete["genres_concatenated"].unique())
kMeans = KMeans(n_clusters=number_of_clusters, random_state=0, n_init=10).fit(X)
df_complete["cluster"] = kMeans.labels_

# Filter out rows with empty genres_concatenated
non_empty_df = df_complete[df_complete["genres_concatenated"] != ""]

# Final cluster labels and genres
final_df = (
    non_empty_df.groupby(["cluster"])["genres_concatenated"]
    .agg(lambda x: pd.Series.mode(x)[0])
    .reset_index()
)

# Identify missing clusters
founded_clusters = final_df["cluster"].tolist()
missing_clusters = list(set(range(number_of_clusters)) - set(founded_clusters))

# Create a DataFrame for missing clusters with the default subject 'Music'
miss_clus_subj = ["Music" for _ in range(len(missing_clusters))]
missing_df = pd.DataFrame(
    {"cluster": missing_clusters, "genres_concatenated": miss_clus_subj}
)

# Concatenate the DataFrames
final_df = pd.concat([final_df, missing_df], ignore_index=True)

empty = df_complete["genres_concatenated"] == ""

df_complete.loc[empty, "genres_concatenated"] = df_complete.loc[empty, "cluster"].apply(
    lambda x: final_df[final_df["cluster"] == x]["genres_concatenated"].values[0]
)

print(df_complete[df_complete["genres_concatenated"] == ""])

df_finale = df_complete[
    ["album", "artist", "description", "link", "img", "genres_concatenated"]
]

album_name = df_complete.album.values
artist_name = df_complete.artist.values
link = df_complete.link.values
img = df_complete.img.values
description = df_complete.description.values
generes_type = df_complete.genres_concatenated.values


# Print final cluster information
# for i, row in final_df.iterrows():
#     print(f"Cluster {row['cluster']}: {row['genres_concatenated']}")
