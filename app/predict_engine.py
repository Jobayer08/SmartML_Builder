import os
import json
import joblib
import numpy as np
import pandas as pd

from PIL import Image
from netCDF4 import Dataset

import torch
from torchvision import models, transforms
from torchvision.models import ResNet18_Weights
from mlops.logger import log_prediction


MODEL_DIR = "models"


# =========================================================
# 🔹 UNIVERSAL MODEL LOADER
# =========================================================
def _find_latest_versioned_model(prefix):
    if not os.path.exists(MODEL_DIR):
        return None

    latest_path = None
    latest_version = 0

    for filename in os.listdir(MODEL_DIR):
        if not filename.endswith(".pkl"):
            continue

        if not filename.startswith(prefix + "_v"):
            continue

        try:
            version = int(filename[len(prefix) + 2:-4])
        except ValueError:
            continue

        if version > latest_version:
            latest_version = version
            latest_path = os.path.join(MODEL_DIR, filename)

    return latest_path


def load_model_path(model_name, model_type=None):

    if model_type == "image":
        for prefix in [f"{model_name}_image", f"{model_name}_cluster"]:
            versioned = _find_latest_versioned_model(prefix)
            if versioned:
                return versioned

        paths = [
            f"{MODEL_DIR}/{model_name}.pkl",
            f"{MODEL_DIR}/{model_name}_image.pkl",
            f"{MODEL_DIR}/{model_name}_cluster.pkl"
        ]

    elif model_type == "nc4":
        versioned = _find_latest_versioned_model(f"{model_name}_nc4")
        if versioned:
            return versioned

        paths = [
            f"{MODEL_DIR}/{model_name}.pkl",
            f"{MODEL_DIR}/{model_name}_nc4.pkl"
        ]

    else:
        versioned = _find_latest_versioned_model(model_name)
        if versioned:
            return versioned

        paths = [
            f"{MODEL_DIR}/{model_name}.pkl"
        ]

    for p in paths:
        if os.path.exists(p):
            return p

    return None


# =========================================================
# 🔹 CNN FEATURE EXTRACTOR
# =========================================================
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

cnn = models.resnet18(weights=ResNet18_Weights.DEFAULT)
cnn.fc = torch.nn.Identity()
cnn.eval()


def extract_features(image_path):
    try:
        img = Image.open(image_path).convert("RGB")
        img = transform(img).unsqueeze(0)

        with torch.no_grad():
            feat = cnn(img)

        return feat.squeeze().cpu().numpy().astype(np.float32)

    except Exception:
        return None


# =========================================================
# 🔹 CSV PREDICTION
# =========================================================
def _find_user_model(user_dir, model_name):
    if not user_dir or not os.path.exists(user_dir):
        return None

    latest = None
    latest_v = 0
    for fn in os.listdir(user_dir):
        if not fn.endswith('.pkl'):
            continue
        if not fn.startswith(model_name + "_v"):
            continue
        try:
            v = int(fn[len(model_name) + 2:-4])
        except Exception:
            v = 0
        if v > latest_v:
            latest_v = v
            latest = os.path.join(user_dir, fn)

    return latest


def predict_csv(model_name, data, user_dir=None, user_id=None):

    # try user-specific model first
    model_path = _find_user_model(user_dir, model_name) if user_dir else None

    if not model_path:
        model_path = load_model_path(model_name, "csv")

    if not model_path:
        return {"error": f"Model {model_name} not found"}

    loaded = joblib.load(model_path)

    # If saved as dict with preprocessor
    if isinstance(loaded, dict) and "model" in loaded:
        model = loaded["model"]
        preprocessor = loaded.get("preprocessor")

        df = pd.DataFrame([data])

        if preprocessor is not None:
            X = preprocessor.transform(df)
        else:
            X = pd.get_dummies(df)

        pred = model.predict(X)

    else:
        # backward compatible: raw model + meta json
        meta_path = f"{MODEL_DIR}/{model_name}_meta.json"
        with open(meta_path) as f:
            meta = json.load(f)

        required_features = meta["features"]

        df = pd.DataFrame([data])
        df = pd.get_dummies(df)

        for col in required_features:
            if col not in df:
                df[col] = 0

        df = df[required_features]

        pred = loaded.predict(df)

    log_prediction(
        model_name,
        "csv",
        pred.tolist(),
        user_id=user_id
    )

    return {
        "type": "csv_prediction",
        "prediction": pred.tolist()
    }


# =========================================================
# 🔥 IMAGE PREDICTION
# =========================================================
def predict_image(model_name, image_path, user_dir=None, user_id=None):
    # prefer user-specific image model if available
    model_path = _find_user_model(user_dir, model_name) if user_dir else None
    if not model_path:
        model_path = load_model_path(model_name, "image")

    if not model_path:
        return {"error": f"Model {model_name} not found"}

    data = joblib.load(model_path)

    features = extract_features(image_path)
    features = np.asarray(features, dtype=np.float32).reshape(1, -1)

    # Classification
    if isinstance(data, dict) and "classes" in data:
        clf = data["model"]
        classes = data["classes"]

        pred = clf.predict(features)[0]

        log_prediction(
            model_name,
            "image_classification",
            str(pred),
            user_id=user_id
        )

        return {
            "type": "image_classification",
            "prediction": str(pred),
            "classes": classes
        }

    # Clustering with examples
    elif isinstance(data, dict) and "examples" in data:
        kmeans = data["model"]
        examples = data["examples"]

        pred = kmeans.predict(features)[0]

        log_prediction(
            model_name,
            "image_cluster",
            int(pred),
            user_id=user_id
        )

        return {
            "type": "image_cluster",
            "cluster_id": int(pred),
            "example_images_in_this_cluster": examples[int(pred)][:5]
        }

    # fallback
    else:
        pred = data.predict(features)[0]

        log_prediction(
            model_name,
            "image_cluster",
            int(pred),
            user_id=user_id
        )

        return {
            "type": "image_cluster",
            "cluster_id": int(pred)
        }


# =========================================================
# 🔥 NC4 PREDICTION (SMART + BACKWARD COMPATIBLE)
# =========================================================
def predict_nc4(model_name, file_path, user_dir=None):
    model_path = _find_user_model(user_dir, model_name) if user_dir else None
    if not model_path:
        model_path = load_model_path(model_name, "nc4")
    if not model_path:
        return {"error": f"Model {model_name} not found"}

    data = joblib.load(model_path)

    # =====================================================
    # 🔹 CASE 1: NEW SMART MODEL (DICT)
    # =====================================================
    if isinstance(data, dict) and "model" in data:

        model = data["model"]
        target = data.get("target", "unknown")
        features = data.get("features", [])
        units = data.get("units", {})

        ds = Dataset(file_path)

        X_arrays = []
        used_features = []

        for f in features:

            if f not in ds.variables:
                continue

            arr = np.array(ds.variables[f][:]).flatten()
            if arr.size == 0:
                continue

            X_arrays.append(arr)
            used_features.append(f)

        ds.close()

        if len(X_arrays) == 0:
            return {"error": "No valid features found"}

        min_length = min(len(arr) for arr in X_arrays)
        if min_length == 0:
            return {"error": "No usable feature samples found"}

        X = np.vstack([arr[:min_length] for arr in X_arrays]).T.astype(np.float64)

        pred = model.predict(X)

        log_prediction(
            model_name,
            "nc4",
            pred[:10].tolist(),
            user_id=user_id
        )

        return {
            "type": "nc4_prediction",
            "target": target,
            "target_unit": units.get(target, "unknown"),
            "used_features": used_features,
            "feature_units": {f: units.get(f, "unknown") for f in used_features},
            "samples_predicted": int(len(pred)),
            "prediction_sample": pred[:10].tolist()
        }

    # =====================================================
    # 🔹 CASE 2: OLD MODEL (meta.json based)
    # =====================================================
    else:

        model = data
        meta_path = f"{MODEL_DIR}/{model_name}_meta.json"

        if not os.path.exists(meta_path):
            return {"error": "Model metadata not found"}

        with open(meta_path) as f:
            meta = json.load(f)

        feature_variables = meta.get("feature_variables", [])

        ds = Dataset(file_path)

        X_list = []

        for var_name in feature_variables:

            if var_name not in ds.variables:
                continue

            try:
                data_arr = ds.variables[var_name][:]
                arr = np.array(data_arr).astype(np.float64)

                if arr.ndim >= 2:
                    feat = arr.mean(axis=tuple(range(1, arr.ndim)))
                else:
                    feat = arr

                X_list.append(feat)

            except Exception:
                continue

        ds.close()

        if len(X_list) == 0:
            return {"error": "No valid features extracted"}

        X = np.vstack(X_list).T

        pred = model.predict(X)

        log_prediction(
            model_name,
            "nc4",
            pred[:10].tolist(),
            user_id=user_id
        )

        return {
            "type": "nc4_prediction",
            "samples_predicted": int(len(pred)),
            "prediction_sample": pred[:10].tolist()
        }


# =========================================================
# 🔹 MODEL LIST
# =========================================================
def list_models():

    if not os.path.exists(MODEL_DIR):
        return []

    return [
        f.replace(".pkl", "")
        for f in os.listdir(MODEL_DIR)
        if f.endswith(".pkl")
    ]