from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from pydantic import BaseModel

import pandas as pd
from io import StringIO
import numpy as np
import zipfile
import os
import shutil
from netCDF4 import Dataset

from app.preprocessing import auto_feature_engineering, auto_split
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

    models = os.listdir(MODEL_DIR)

    return {
        "available_models": models
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
        raise HTTPException(
            status_code=400,
            detail="Only CSV or ZIP files supported"
        )


# ====================================
# STEP 2 — FEATURE ENGINEERING
# ====================================
@app.post("/feature-engineering/")
async def feature_engineering(
    target_column: str = Form(...),
    file: UploadFile = File(...)
):

    contents = await file.read()

    df = pd.read_csv(
        StringIO(contents.decode("utf-8")),
        low_memory=False
    )

    X, y = auto_feature_engineering(df, target_column)

    X_train, X_test, y_train, y_test = auto_split(X, y)

    return {
        "features": list(X.columns),
        "feature_count": len(X.columns),
        "train_rows": len(X_train),
        "test_rows": len(X_test)
    }


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

    # ==================
    # CSV TRAINING
    # ==================
    if filename.endswith(".csv"):

        if not target_column:
            raise HTTPException(400, "target_column required")

        contents = await file.read()

        df = pd.read_csv(
            StringIO(contents.decode("utf-8")),
            low_memory=False
        )

        X, y = auto_feature_engineering(df, target_column)

        X_train, X_test, y_train, y_test = auto_split(
            X, y
        )

        result = train_models(
            X_train,
            X_test,
            y_train,
            y_test
        )

        return {
            "dataset_type": "csv",
            "model_name": model_name,
            "target": target_column,
            "training_result": result
        }

    # ==================
    # ZIP DATASET
    # ==================
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

                if name.endswith(".csv"):
                    csv_files.append(path)

                elif name.lower().endswith((".jpg", ".png", ".jpeg")):
                    image_files.append(path)

                elif name.endswith(".nc4"):
                    nc4_files.append(path)

        dataset_type = detect_dataset(
            csv_files,
            image_files,
            nc4_files
        )

        # IMAGE CLASSIFICATION
        if dataset_type == "image_labeled":

            result = train_labeled_images(
                EXTRACT_DIR,
                model_name
            )

            return {
                "dataset_type": dataset_type,
                "model_name": model_name,
                "result": result
            }

        # IMAGE CLUSTERING
        if dataset_type == "image_unlabeled":

            result = cluster_images(EXTRACT_DIR)

            return {
                "dataset_type": dataset_type,
                "result": result
            }

        # NC4 TRAINING
        if dataset_type == "nc4":

            result = analyze_nc4(
                nc4_files[0],
                target_column,
                model_name
            )

            return {
                "dataset_type": dataset_type,
                "model_name": model_name,
                "result": result
            }

        return {"dataset_type": "unknown"}

    else:

        raise HTTPException(
            status_code=400,
            detail="Unsupported file format"
        )


# ====================================
# STEP 4 — PREDICTION API
# ====================================

class CSVPrediction(BaseModel):
    model_name: str
    data: dict


# CSV Prediction
@app.post("/predict-csv/")
async def predict_csv_api(input: CSVPrediction):

    result = predict_csv(
        input.model_name,
        input.data
    )

    return result


# Image Prediction
@app.post("/predict-image/")
async def predict_image_api(
    model_name: str = Form(...),
    file: UploadFile = File(...)
):

    path = f"{UPLOAD_DIR}/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    result = predict_image(
        model_name,
        path
    )

    return result


# NC4 Prediction
@app.post("/predict-nc4/")
async def predict_nc4_api(
    model_name: str = Form(...),
    file: UploadFile = File(...)
):

    path = f"{UPLOAD_DIR}/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    result = predict_nc4(
        model_name,
        path
    )

    return result