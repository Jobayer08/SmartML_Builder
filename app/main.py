from fastapi import FastAPI, File, UploadFile, HTTPException
import pandas as pd
from io import StringIO
import numpy as np
import zipfile
import os
import shutil
from netCDF4 import Dataset

from app.preprocessing import auto_feature_engineering, auto_split
from fastapi import Form


app = FastAPI()

UPLOAD_DIR = "data/uploads"
EXTRACT_DIR = "data/extracted"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"status": "SmartML Builder Step 1 Running"}

@app.post("/upload-dataset/")
async def upload_dataset(file: UploadFile = File(...)):

    filename = file.filename.lower()

    # =========================
    # CASE 1 — CSV Upload
    # =========================
    if filename.endswith(".csv"):
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode("utf-8")))

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

    # =========================
    # CASE 2 — ZIP Upload
    # =========================
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

        # Scan nested folders
        for root, _, files in os.walk(EXTRACT_DIR):
            for name in files:
                path = os.path.join(root, name)

                if name.lower().endswith(".csv"):
                    csv_files.append(path)

                elif name.lower().endswith((".jpg", ".jpeg", ".png")):
                    image_files.append(path)

                elif name.lower().endswith(".nc4"):
                    nc4_files.append(path)

        result = {
            "dataset_type": "ZIP",
            "csv_files_found": len(csv_files),
            "image_files_found": len(image_files),
            "nc4_files_found": len(nc4_files),
            "sample_images": image_files[:5],
            "sample_nc4": nc4_files[:3]
        }

        # -------------------
        # Process CSV if exists
        # -------------------
        if csv_files:
            df = pd.read_csv(csv_files[0])
            df = df.drop_duplicates()
            df = df.ffill()

            preview = df.head(5).replace({np.nan: None}).to_dict()
            summary = df.describe(include="all").replace({np.nan: None}).to_dict()

            result["rows"] = int(len(df))
            result["columns"] = list(df.columns)
            result["preview"] = preview
            result["summary"] = summary

        # -------------------
        # Process NC4 if exists
        # -------------------
        if nc4_files:
            sample_nc4 = nc4_files[0]

            nc_data = Dataset(sample_nc4, "r")

            variables = list(nc_data.variables.keys())
            dimensions = list(nc_data.dimensions.keys())

            result["nc4_metadata"] = {
                "variables": variables[:15],
                "dimensions": dimensions,
                "file_sample": os.path.basename(sample_nc4)
            }

            nc_data.close()

        return result

    # =========================
    # Unsupported File
    # =========================
    else:
        raise HTTPException(
            status_code=400,
            detail="Only CSV, ZIP, JPG, PNG, or NC4 files are supported"
        )
    

@app.post("/feature-engineering/")
async def feature_engineering(
    target_column: str = Form(...),
    file: UploadFile = File(...)
):
    filename = file.filename.lower()

    # CSV direct
    if filename.endswith(".csv"):
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode("utf-8")))

    # ZIP containing CSV
    elif filename.endswith(".zip"):
        zip_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(zip_path, "wb") as f:
            f.write(await file.read())

        shutil.rmtree(EXTRACT_DIR, ignore_errors=True)
        os.makedirs(EXTRACT_DIR, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(EXTRACT_DIR)

        csv_file = None
        for root, _, files in os.walk(EXTRACT_DIR):
            for name in files:
                if name.lower().endswith(".csv"):
                    csv_file = os.path.join(root, name)
                    break

        if csv_file is None:
            raise HTTPException(status_code=400, detail="No CSV found inside ZIP")

        df = pd.read_csv(csv_file)

    else:
        raise HTTPException(status_code=400, detail="Only CSV or ZIP allowed")

    # Apply feature engineering
    processed_df = auto_feature_engineering(df)

    X_train, X_test, y_train, y_test = auto_split(processed_df, target_column)

    return {
        "processed_shape": processed_df.shape,
        "train_rows": len(X_train),
        "test_rows": len(X_test),
        "columns_after_processing": list(processed_df.columns)
    }

