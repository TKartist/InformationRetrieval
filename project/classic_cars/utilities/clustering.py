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

# Stemming Lib
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

nltk.download("punkt")


# In case we want to visualize the clustered data
def clustering_visualization(X, clustering_labels):
    tsne = TSNE(random_state=0)
    X_reduced = tsne.fit_transform(X.toarray())
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(
        X_reduced
    )  # clustering in the reduced space

    clustering_labels = kmeans.labels_

    plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=clustering_labels)


#############################################################################
#                                                                           #
#                           Assuming Indexing is done                       #
#                           Before clustering is done                       #
#                                                                           #
#############################################################################


# Reading Data
# car_parse_array = jsonReader(INDEXPATH)
# x = pd.DataFrame(car_parse_array)
# data = pd.read_json(INDEXPATH)
# texts = data["text"].str.lower()

# stemming

vectorizer = TfidfVectorizer(
    stop_words="english", max_df=0.9, min_df=0.01, max_features=1000
)
n_clusters = 10


def apply_stem(text, stemmer):
    words = word_tokenize(text)
    stemmed_text = " ".join([stemmer.stem(word) for word in words])
    return stemmed_text


# Assuming data is a DF structure with docNo, brand, model, year, price, text etc.
def perform_clustering(data):
    stemmer = PorterStemmer()
    texts = data["text"].str.lower()
    stemmed_text = [apply_stem(str(text), stemmer) for text in texts]
    X = vectorizer.fit_transform(stemmed_text)
    # K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init=10).fit(X)

    # dbscan = DBSCAN().fit(X) # for DBSCAN method
    clustering_labels = kmeans.labels_  # clustering labels


# For viewing the DF form of the cluster
# k = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
# clustering_visualization(X, clustering_labels)
