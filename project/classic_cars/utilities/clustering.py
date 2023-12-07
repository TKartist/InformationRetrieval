import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Generate some sample data
np.random.seed(42)
data = np.concatenate(
    [np.random.normal(0, 1, (100, 2)), np.random.normal(5, 1, (100, 2))]
)

# Specify the number of clusters
num_clusters = 2

# Apply K-Means clustering
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
labels = kmeans.fit_predict(data)

# Separate data points based on cluster labels
clustered_data = [data[labels == i] for i in range(num_clusters)]

# Plot the clustered data
colors = ["r", "b"]
for i in range(num_clusters):
    plt.scatter(
        clustered_data[i][:, 0],
        clustered_data[i][:, 1],
        c=colors[i],
        label=f"Cluster {i + 1}",
    )

# Plot centroids
plt.scatter(
    kmeans.cluster_centers_[:, 0],
    kmeans.cluster_centers_[:, 1],
    c="black",
    marker="x",
    s=200,
    label="Centroids",
)

plt.title("K-Means Clustering")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.legend()
plt.show()
