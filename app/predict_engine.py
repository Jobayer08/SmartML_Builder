import joblib
import pandas as pd
import torch
import numpy as np
from PIL import Image
from torchvision import transforms

# =========================
# CSV Prediction
# =========================

def predict_csv(data):

    model = joblib.load("models/best_csv_model.pkl")

    df = pd.DataFrame([data])

    df = pd.get_dummies(df)

    pred = model.predict(df)

    return {
        "type": "csv_prediction",
        "prediction": pred.tolist()
    }


# =========================
# Image Prediction
# =========================

def predict_image(image_path):

    model = torch.load("models/image_model.pth")

    transform = transforms.Compose([
        transforms.Resize((64,64)),
        transforms.ToTensor()
    ])

    img = Image.open(image_path)

    img = transform(img).unsqueeze(0)

    output = model(img)

    pred = torch.argmax(output,1).item()

    return {
        "type": "image_prediction",
        "predicted_class": pred
    }


# =========================
# NC4 Prediction
# =========================

def predict_nc4(file_path):

    model = joblib.load("models/nc4_model.pkl")

    mean = model["mean"]
    std = model["std"]

    return {
        "type": "nc4_analysis",
        "mean": mean,
        "std": std
    }