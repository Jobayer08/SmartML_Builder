from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from pydantic import BaseModel

import pandas as pd
from io import StringIO
import numpy as np
import zipfile
import os
import shutil
import json
from netCDF4 import Dataset

from app.preprocessing import smart_preprocessing, auto_split
from app.ml_engine import train_models
from app.image_engine import train_labeled_images
from app.clustering_engine import cluster_images
from app.nc4_engine import analyze_nc4
from app.predict_engine import predict_csv, predict_image, predict_nc4


app = FastAPI()

UPLOAD_DIR = "data/uploads"
EXTRACT_DIR = "data/extracted"
MODEL_DIR = "models"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)


# ==============================
# ROOT
# ==============================
@app.get("/")
async def root():
    return {"status": "SmartML Builder Running"}


# ==============================
# MODEL REGISTRY
# ==============================
@app.get("/models/")
def list_models():

    models = []

    for f in os.listdir(MODEL_DIR):

        if f.endswith(".pkl"):
            models.append(f.replace(".pkl", ""))

    return {
        "available_models": models
    }


# ==============================
# 🔥 NEW: MODEL INFO API
# ==============================
@app.get("/model-info/{model_name}")
def model_info(model_name: str):

    meta_path = os.path.join(MODEL_DIR, f"{model_name}_meta.json")

    if not os.path.exists(meta_path):
        raise HTTPException(404, "Model metadata not found")

    with open(meta_path) as f:
        meta = json.load(f)

    # CSV model case
    if "features" in meta and "target" in meta:

        features = meta["features"]
        target = meta["target"]

        example = {}

        for f in features:

            # simple smart example generation
            if "id" in f.lower():
                example[f] = 1
            elif "name" in f.lower():
                example[f] = "example"
            else:
                example[f] = 0

        return {
            "model_name": model_name,
            "dataset_type": "csv",
            "target": target,
            "required_features": features,
            "example_input": example
        }

    # NC4 model case
    elif meta.get("dataset_type") == "nc4":

        return {
            "model_name": model_name,
            "dataset_type": "nc4",
            "target_variable": meta.get("target_variable"),
            "feature_variables": meta.get("feature_variables"),
            "message": "Upload .nc4 file for prediction"
        }

    # Image model case
    else:

        return {
            "model_name": model_name,
            "dataset_type": "image",
            "message": "Upload image file for prediction"
        }


# ==============================
# DATASET DETECTION ENGINE
# ==============================
def detect_dataset(csv_files, image_files, nc4_files):

    if nc4_files:
        return "nc4"

    if image_files:

        folders = set()

        for path in image_files:
            folders.add(os.path.dirname(path))

        if len(folders) > 1:
            return "image_labeled"
        else:
            return "image_unlabeled"

    if csv_files:
        return "csv"

    return "unknown"


# ====================================
# STEP 1 — DATASET UPLOAD
# ====================================
@app.post("/upload-dataset/")
async def upload_dataset(file: UploadFile = File(...)):

    filename = file.filename.lower()

    if filename.endswith(".csv"):

        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode("utf-8")), low_memory=False)

        df = df.drop_duplicates()
        df = df.ffill()

        preview = df.head(5).replace({np.nan: None}).to_dict()
        summary = df.describe(include="all").replace({np.nan: None}).to_dict()

        return {
            "dataset_type": "CSV",
            "rows": int(len(df)),
            "columns": list(df.columns),
            "preview": preview,
            "summary": summary
        }

    elif filename.endswith(".zip"):

        zip_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(zip_path, "wb") as f:
            f.write(await file.read())

        shutil.rmtree(EXTRACT_DIR, ignore_errors=True)
        os.makedirs(EXTRACT_DIR, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(EXTRACT_DIR)

        csv_files = []
        image_files = []
        nc4_files = []

        for root, _, files in os.walk(EXTRACT_DIR):

            for name in files:

                path = os.path.join(root, name)

                if name.lower().endswith(".csv"):
                    csv_files.append(path)

                elif name.lower().endswith((".jpg", ".jpeg", ".png")):
                    image_files.append(path)

                elif name.lower().endswith(".nc4"):
                    nc4_files.append(path)

        dataset_type = detect_dataset(csv_files, image_files, nc4_files)

        result = {
            "dataset_type": dataset_type,
            "csv_files": len(csv_files),
            "images": len(image_files),
            "nc4_files": len(nc4_files)
        }

        if nc4_files:

            nc_data = Dataset(nc4_files[0])
            variables = list(nc_data.variables.keys())
            nc_data.close()

            result["nc4_variables"] = variables

        return result

    else:
        raise HTTPException(400, "Only CSV or ZIP files supported")


# ====================================
# STEP 2 — FEATURE ENGINEERING
# ====================================
@app.post("/feature-engineering/")
async def feature_engineering(
    file: UploadFile = File(...),
    target_column: str = Form(None)
):

    filename = file.filename.lower()

    if filename.endswith(".csv"):

        if not target_column:
            raise HTTPException(400, "target_column required for CSV")

        contents = await file.read()

        df = pd.read_csv(
            StringIO(contents.decode("utf-8")),
            low_memory=False
        )

        X, y = smart_preprocessing(df, target_column)
        X_train, X_test, y_train, y_test = auto_split(X, y)

        return {
            "dataset_type": "csv",
            "features": list(X.columns),
            "feature_count": len(X.columns),
            "train_rows": len(X_train),
            "test_rows": len(X_test)
        }

    elif filename.endswith(".zip"):

        return {
            "dataset_type": "non-csv",
            "message": "Feature engineering not required for Image or NC4 datasets"
        }

    else:
        raise HTTPException(400, "Unsupported file format")


# ====================================
# STEP 3 — MODEL TRAINING
# ====================================
@app.post("/train-model/")
async def train_model(
    file: UploadFile = File(...),
    target_column: str = Form(None),
    model_name: str = Form("default_model")
):

    filename = file.filename.lower()

    if filename.endswith(".csv"):

        if not target_column:
            raise HTTPException(400, "target_column required")

        contents = await file.read()

        df = pd.read_csv(
            StringIO(contents.decode("utf-8")),
            low_memory=False
        )

        X, y = smart_preprocessing(df, target_column)
        X_train, X_test, y_train, y_test = auto_split(X, y)

        result = train_models(
            X_train,
            X_test,
            y_train,
            y_test,
            features=list(X.columns),
            target=target_column,
            model_name=model_name
        )

        return {
            "dataset_type": "csv",
            "model_name": model_name,
            "target": target_column,
            "training_result": result
        }

    elif filename.endswith(".zip"):

        zip_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(zip_path, "wb") as f:
            f.write(await file.read())

        shutil.rmtree(EXTRACT_DIR, ignore_errors=True)
        os.makedirs(EXTRACT_DIR, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(EXTRACT_DIR)

        csv_files, image_files, nc4_files = [], [], []

        for root, _, files in os.walk(EXTRACT_DIR):
            for name in files:
                path = os.path.join(root, name)

                if name.endswith(".csv"):
                    csv_files.append(path)
                elif name.lower().endswith((".jpg", ".png", ".jpeg")):
                    image_files.append(path)
                elif name.endswith(".nc4"):
                    nc4_files.append(path)

        dataset_type = detect_dataset(csv_files, image_files, nc4_files)

        if dataset_type == "image_labeled":

            return {
                "dataset_type": dataset_type,
                "model_name": model_name,
                "result": train_labeled_images(EXTRACT_DIR, model_name)
            }

        if dataset_type == "image_unlabeled":

            return {
                "dataset_type": dataset_type,
                "model_name": model_name,
                "result": cluster_images(EXTRACT_DIR, model_name)
            }

        if dataset_type == "nc4":

            return {
                "dataset_type": dataset_type,
                "model_name": model_name,
                "result": analyze_nc4(nc4_files[0], target_column, model_name)
            }

        return {"dataset_type": "unknown"}

    else:
        raise HTTPException(400, "Unsupported file format")


# ====================================
# STEP 4 — PREDICTION API
# ====================================
class CSVPrediction(BaseModel):
    model_name: str
    data: dict


@app.post("/predict-csv/")
async def predict_csv_api(input: CSVPrediction):
    return predict_csv(input.model_name, input.data)


@app.post("/predict-image/")
async def predict_image_api(
    model_name: str = Form(...),
    file: UploadFile = File(...)
):
    path = f"{UPLOAD_DIR}/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    return predict_image(model_name, path)


@app.post("/predict-nc4/")
async def predict_nc4_api(
    model_name: str = Form(...),
    file: UploadFile = File(...)
):
    path = f"{UPLOAD_DIR}/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    return predict_nc4(model_name, path)

