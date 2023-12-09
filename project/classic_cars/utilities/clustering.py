# Matlab and Pandas libs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("ggplot")
import re
import sklearn
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans, DBSCAN
from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# Personal lib
from file_paths import INDEXPATH
from indexerScript import jsonReader

# Stemming Lib
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

nltk.download("punkt")
# Reading Data
# car_parse_array = jsonReader(INDEXPATH)
# x = pd.DataFrame(car_parse_array)
data = pd.read_json(INDEXPATH)
texts = data["text"].str.lower()


# removing irregular texts
def cleaned_func(text):
    text = re.sub(r"\(.*?\)", "", text)  # remove elements inside ()
    text = re.sub(r"\[.*?\]", "", text)  # remove elements inside []
    # text = re.sub(r'lyrics from.*?$', '', text, flags=re.IGNORECASE)  # remove "lyrics from" sentences
    text = re.sub(r"\\", "", text)  # remove \
    text = re.sub(r"-", "", text)  # remove -
    text = re.sub(r"\n", "", text)  # remove
    text = re.sub(
        r"\s+", " ", text
    ).strip()  # Remove multiple spaces at the beginning and at the end of the sentences
    return text


cleaned_text = [cleaned_func(str(text)) for text in texts]

# stemming
stemmer = PorterStemmer()


def apply_stem(text, stemmer):
    words = word_tokenize(text)
    stemmed_text = " ".join([stemmer.stem(word) for word in words])
    return stemmed_text


stemmed_text = [apply_stem(str(text), stemmer) for text in texts]

vectorizer = TfidfVectorizer(
    stop_words="english", max_df=0.9, min_df=0.01, max_features=1000
)

X = vectorizer.fit_transform(stemmed_text)

# K-Means
n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(X)
# dbscan = DBSCAN().fit(X)

clustering_labels = kmeans.labels_  # clustering labels

k = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
k.to_csv("clustered.csv", index=False, encoding="utf-8")


def clustering_visualization(X, clustering_labels):
    tsne = TSNE(random_state=0)
    X_reduced = tsne.fit_transform(X.toarray())
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(
        X_reduced
    )  # clustering in the reduced space

    clustering_labels = kmeans.labels_

    plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=clustering_labels)
    plt.show()


clustering_visualization(X, clustering_labels)
