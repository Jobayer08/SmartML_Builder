import joblib
import json
import pandas as pd
import torch
import torchvision
import numpy as np
from PIL import Image
from torchvision import transforms
from netCDF4 import Dataset
import os

MODEL_DIR = "models"


# ===================================
# CSV PREDICTION (MULTI MODEL)
# ===================================

def predict_csv(model_name, data):

    model_path = f"{MODEL_DIR}/{model_name}.pkl"
    meta_path = f"{MODEL_DIR}/{model_name}_meta.json"

    if not os.path.exists(model_path):
        raise Exception("CSV model not found")

    if not os.path.exists(meta_path):
        raise Exception("Model metadata not found")

    model = joblib.load(model_path)

    with open(meta_path) as f:
        meta = json.load(f)

    required_features = meta["features"]

    df = pd.DataFrame([data])

    df = pd.get_dummies(df)

    # missing feature fix
    for col in required_features:
        if col not in df:
            df[col] = 0

    df = df[required_features]

    pred = model.predict(df)

    return {
        "type": "csv_prediction",
        "model": model_name,
        "prediction": pred.tolist()
    }


# ===================================
# IMAGE PREDICTION (MULTI MODEL)
# ===================================

def predict_image(model_name, image_path):

    model_path = f"{MODEL_DIR}/{model_name}.pth"

    if not os.path.exists(model_path):
        raise Exception("Image model not found")

    checkpoint = torch.load(model_path)

    classes = checkpoint["classes"]

    model = torchvision.models.resnet18()

    model.fc = torch.nn.Linear(
        model.fc.in_features,
        len(classes)
    )

    model.load_state_dict(checkpoint["model_state"])

    model.eval()

    transform = transforms.Compose([
        transforms.Resize((128,128)),
        transforms.ToTensor()
    ])

    image = Image.open(image_path).convert("RGB")

    img = transform(image).unsqueeze(0)

    with torch.no_grad():

        outputs = model(img)

        _, predicted = torch.max(outputs, 1)

    return {
        "type": "image_prediction",
        "model": model_name,
        "prediction": classes[predicted.item()]
    }


# ===================================
# NC4 PREDICTION (MULTI MODEL)
# ===================================

def predict_nc4(model_name, file_path):

    model_path = f"{MODEL_DIR}/{model_name}.pkl"

    if not os.path.exists(model_path):
        raise Exception("NC4 model not found")

    model = joblib.load(model_path)

    nc_data = Dataset(file_path)

    features = []

    for var in nc_data.variables:

        try:
            arr = nc_data.variables[var][:].flatten()
            features.append(arr)
        except:
            continue

    nc_data.close()

    X = np.array(features).T

    try:
        pred = model.predict(X)

        return {
            "type": "nc4_prediction",
            "model": model_name,
            "prediction_sample": pred[:10].tolist()
        }

    except:

        return {
            "type": "nc4_analysis",
            "model": model_name,
            "message": "Model prediction not possible, returning dataset stats"
        }


# ===================================
# MODEL LIST FUNCTION
# ===================================

def list_models():

    if not os.path.exists(MODEL_DIR):
        return []

    models = os.listdir(MODEL_DIR)

    return models