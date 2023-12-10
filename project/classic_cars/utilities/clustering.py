# Matlab and Pandas libs
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("ggplot")
import sklearn
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import TfidfVectorizer

# Stemming Lib
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# Pre-build
nltk.download("punkt")
vectorizer = TfidfVectorizer(
    stop_words="english", max_df=0.9, min_df=0.01, max_features=1000
)


# In case we want to visualize the clustered data
def clustering_visualization(X, n_clusters):
    tsne = TSNE(random_state=0)
    X_reduced = tsne.fit_transform(X.toarray())
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(
        X_reduced
    )  # clustering in the reduced space

    clustering_labels = kmeans.labels_

    plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=clustering_labels)
    plt.show()


#############################################################################
#                                                                           #
#                           Assuming Indexing is done                       #
#                           Before clustering is done                       #
#                                                                           #
#############################################################################


# Stemming
def apply_stem(text, stemmer):
    words = word_tokenize(text)
    stemmed_text = " ".join([stemmer.stem(word) for word in words])
    return stemmed_text


def convertPd2JList(inp):
    out = []
    for x in inp:
        out.append(
            {
                "docno": x["docno"],
                "price": x["price"],
                "brand": x["brand"],
                "model": x["model"],
                "year": x["year"],
                "text": x["text"],
                "image_url": x["image_url"],
                "detail_url": x["detail_url"],
            }
        )
    return out


# Assuming data is a DF structure with docNo, brand, model, year, price, text etc.
def perform_clustering(data):
    print("...Starting the clustering using K-Mean Method...")
    stemmer = PorterStemmer()
    texts = data["text"].str.lower()
    stemmed_text = [apply_stem(str(text), stemmer) for text in texts]
    X = vectorizer.fit_transform(stemmed_text)
    n_clusters = len(data["brand"].unique())

    # Please uncomment the line below and run "python trial.py" command in utilities directory
    # to view the scatter graph of clustering
    # clustering_visualization(X, n_clusters)

    # K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init=10).fit(X)
    data["clusters"] = kmeans.labels_  # clustering labels
    print("...Labeling Done...")

    # In case indexing is not done
    if data["score"]:
        # Assign the mean score of the cluster group the row belongs to
        data["mean_score"] = data.groupby("clusters")["score"].transform("mean")

        # Sort according to that new mean_score, realistically
        # group with higher mean is likely to have more favorable result
        output = data.sort_values(["mean_score", "score"], ascending=[False, False])
        output = output.drop(columns=["mean_score"])
        output.to_csv(
            "cache_cluster_result.csv"
        )  # stores the most recent clustered query result in cache_cluster_result.csv file
        out = convertPd2JList(output)
    print("Clustering Done...")
    return out
