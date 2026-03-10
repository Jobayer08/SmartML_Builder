import os
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image


def cluster_images(folder):

    features = []
    valid_images = 0

    # =========================
    # Read images
    # =========================
    for img in os.listdir(folder):

        path = os.path.join(folder, img)

        try:
            image = Image.open(path).convert("RGB").resize((64, 64))
            arr = np.array(image).flatten()

            features.append(arr)
            valid_images += 1

        except Exception:
            # Skip invalid files
            continue

    # =========================
    # Check image count
    # =========================
    if valid_images == 0:
        return {
            "task": "image_clustering",
            "error": "No valid images found"
        }

    # number of clusters
    clusters = min(3, valid_images)

    # If less than 2 images clustering useless
    if valid_images < 2:
        return {
            "task": "image_clustering",
            "images": int(valid_images),
            "error": "Not enough images for clustering"
        }

    # =========================
    # Train clustering model
    # =========================
    features = np.array(features)

    kmeans = KMeans(n_clusters=clusters, random_state=42)

    kmeans.fit(features)

    labels = kmeans.labels_

    # =========================
    # Count images per cluster
    # =========================
    cluster_counts = {}

    for label in labels:
        cluster_counts[int(label)] = cluster_counts.get(int(label), 0) + 1

    # =========================
    # Return result
    # =========================
    return {
        "task": "image_clustering",
        "images": int(valid_images),
        "clusters": int(clusters),
        "cluster_distribution": cluster_counts,
        "status": "Clustering completed"
    }