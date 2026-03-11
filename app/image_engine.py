import os
import numpy as np
from PIL import Image
from torchvision import transforms, datasets
from torch.utils.data import DataLoader
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.cluster import KMeans
import joblib


# -----------------------------
# Model save directory
# -----------------------------
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)


# -----------------------------
# Check dataset type
# -----------------------------
def detect_image_dataset_type(dataset_path):

    subfolders = [
        f for f in os.listdir(dataset_path)
        if os.path.isdir(os.path.join(dataset_path, f))
    ]

    if len(subfolders) > 0:
        return "labeled"

    return "unlabeled"


# -----------------------------
# Train labeled image dataset
# -----------------------------
def train_labeled_images(dataset_path):

    transform = transforms.Compose([
        transforms.Resize((64,64)),
        transforms.ToTensor()
    ])

    dataset = datasets.ImageFolder(dataset_path, transform=transform)

    loader = DataLoader(dataset, batch_size=16, shuffle=True)

    model = nn.Sequential(
        nn.Flatten(),
        nn.Linear(64*64*3,128),
        nn.ReLU(),
        nn.Linear(128,len(dataset.classes))
    )

    loss_fn = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(2):

        for images, labels in loader:

            outputs = model(images)
            loss = loss_fn(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    # -----------------------------
    # Save trained image model
    # -----------------------------
    model_path = os.path.join(MODEL_DIR, "image_classifier.pth")

    torch.save({
        "model_state_dict": model.state_dict(),
        "classes": dataset.classes
    }, model_path)

    return {
        "task": "image_classification",
        "classes": dataset.classes,
        "total_images": len(dataset),
        "model_saved": model_path,
        "status": "Image model trained and saved"
    }


# -----------------------------
# Cluster unlabeled images
# -----------------------------
def cluster_unlabeled_images(folder):

    features = []
    image_count = 0

    for file in os.listdir(folder):

        path = os.path.join(folder, file)

        try:
            img = Image.open(path).resize((64,64))
            arr = np.array(img).flatten()

            features.append(arr)
            image_count += 1

        except:
            pass

    if len(features) == 0:
        return {"error": "No valid images found"}

    kmeans = KMeans(n_clusters=3)
    kmeans.fit(features)

    # -----------------------------
    # Save clustering model
    # -----------------------------
    model_path = os.path.join(MODEL_DIR, "image_cluster_model.pkl")

    joblib.dump(kmeans, model_path)

    return {
        "task": "image_clustering",
        "clusters": 3,
        "total_images": image_count,
        "model_saved": model_path,
        "status": "Images clustered and model saved"
    }


# -----------------------------
# Main image training function
# -----------------------------
def train_image_model(dataset_path):

    dataset_type = detect_image_dataset_type(dataset_path)

    if dataset_type == "labeled":

        return train_labeled_images(dataset_path)

    else:

        return cluster_unlabeled_images(dataset_path)