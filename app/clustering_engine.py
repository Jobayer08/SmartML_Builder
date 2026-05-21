import os
import numpy as np
from PIL import Image
import torch
from torchvision import models, transforms
from torchvision.models import ResNet18_Weights
from sklearn.cluster import KMeans
from mlops.versioning import get_versioned_model_path, register_model
import joblib


MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

cnn = models.resnet18(weights=ResNet18_Weights.DEFAULT)
cnn.fc = torch.nn.Identity()
cnn.eval()


def extract_features(img_path):
    
    try:
        img = Image.open(img_path).convert("RGB")
        img = transform(img).unsqueeze(0)

        with torch.no_grad():
            features = cnn(img)

        return features.squeeze().cpu().numpy().astype(np.float32)

    except Exception:
        return None



# IMAGE CLUSTERING

def cluster_images(data_dir, model_name="image_cluster"):
    """
    Cluster unlabeled images using K-means on CNN features.
    Handles nested directory structures recursively.
    """
    features = []
    image_paths = []

    
    for root, _, files in os.walk(data_dir):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                path = os.path.join(root, file)
                feat = extract_features(path)

                if feat is not None:
                    features.append(feat)
                    image_paths.append(path)

    total_images = len(features)

    if total_images < 2:
        return {
            "task": "image_clustering",
            "error": "Not enough valid images (minimum 2 required)"
        }

    X = np.array(features, dtype=np.float32)

    # Determine optimal number of clusters
    clusters = min(5, total_images)

    
    kmeans = KMeans(n_clusters=clusters, random_state=42)
    kmeans.fit(X)

    labels = kmeans.labels_

    # Organize images by cluster
    cluster_examples = {i: [] for i in range(clusters)}
    for path, label in zip(image_paths, labels):
        cluster_examples[int(label)].append(path)

    model_path, version = get_versioned_model_path(f"{model_name}_cluster")

    joblib.dump({
        "model": kmeans,
        "examples": cluster_examples
    }, model_path)

    register_model(
        model_name=model_name,
        model_type="image",
        version=version
    )

    return {
        "task": "image_clustering",
        "images": total_images,
        "clusters": clusters,
        "model_saved_path": model_path,
        "version": version,
        "status": "Clustering completed with examples"
    }