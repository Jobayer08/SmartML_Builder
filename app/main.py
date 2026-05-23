from fastapi import (
    FastAPI,
    File,
    UploadFile,
    HTTPException,
    Form,
    Request,
    Depends
)

from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from pydantic import BaseModel

import pandas as pd
from io import StringIO
import numpy as np
import zipfile
import os
import shutil
import json

from netCDF4 import Dataset

from app.preprocessing import (
    smart_preprocessing,
    auto_split
)

from app.ml_engine import train_models
from app.image_engine import train_labeled_images
from app.clustering_engine import cluster_images
from app.nc4_engine import analyze_nc4

from app.predict_engine import (
    predict_csv,
    predict_image,
    predict_nc4
)

from mlops.logger import log_api
from app.tracker import log_api_usage

from mlops.db import (
    init_db,
    create_user,
    get_user_by_email,
    get_user_by_id
)

from app.schemas import (
    RegisterRequest,
    LoginRequest
)

from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

from mlops.dataset_utils import (
    detect_dataset_type,
    get_file_size_mb
)

from mlops.db import insert_dataset

from mlops.db import get_user_datasets



# ======================================================
# APP
# ======================================================

app = FastAPI()

init_db()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


# ======================================================
# JWT SETTINGS
# ======================================================

SECRET_KEY = "SMARTML_SECRET_KEY"
ALGORITHM = "HS256"


# ======================================================
# API TRACKING MIDDLEWARE
# ======================================================

@app.middleware("http")
async def track_api_requests(
    request: Request,
    call_next
):

    response = await call_next(request)

    ignored = [
        "/docs",
        "/openapi.json",
        "/redoc"
    ]

    if request.url.path not in ignored:

        log_api_usage(
            endpoint=request.url.path,
            method=request.method
        )

    return response


# ======================================================
# DIRECTORIES
# ======================================================

UPLOAD_DIR = "data/uploads"
EXTRACT_DIR = "data/extracted"
MODEL_DIR = "models"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)


# ======================================================
# ROOT
# ======================================================

@app.get("/")
async def root():

    return {
        "status": "SmartML Builder Running"
    }


# ======================================================
# REGISTER
# ======================================================

@app.post("/register")
def register(user: RegisterRequest):

    existing = get_user_by_email(user.email)

    if existing:

        return {
            "error": "Email already registered"
        }

    hashed = hash_password(user.password)

    create_user(
        username=user.username,
        email=user.email,
        password=hashed
    )

    return {
        "message": "User registered successfully"
    }


# ======================================================
# LOGIN
# ======================================================

@app.post("/login")
def login(data: LoginRequest):

    user = get_user_by_email(data.email)

    if not user:

        return {
            "error": "Invalid email"
        }

    valid = verify_password(
        data.password,
        user["password"]
    )

    if not valid:

        return {
            "error": "Invalid password"
        }

    access_token = create_access_token({
        "user_id": user["id"],
        "email": user["email"]
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# ======================================================
# MY MODELS
# ======================================================

@app.get("/my-models")
def my_models(token: str):

    from mlops.db import get_user_models

    user = get_current_user(token)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    models = get_user_models(user["id"])

    result = []
    for m in models:
        result.append({
            "id": m["id"],
            "model_name": m["model_name"],
            "model_type": m["model_type"],
            "created_at": m["created_at"]
        })

    return {
        "user": user["username"],
        "total_models": len(result),
        "models": result
    }


# ======================================================
# PROTECTED ROUTE
# ======================================================

@app.get("/my-profile")
def my_profile(token: str):

    user = get_current_user(token)

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"]
    }


# ======================================================
# MODEL REGISTRY
# ======================================================

@app.get("/models/")
def list_models():

    models = []

    for f in os.listdir(MODEL_DIR):

        if f.endswith(".pkl"):

            models.append(
                f.replace(".pkl", "")
            )

    return {
        "available_models": models
    }


# ======================================================
# MODEL INFO
# ======================================================

@app.get("/model-info/{model_name}")
def model_info(model_name: str):

    meta_path = os.path.join(
        MODEL_DIR,
        f"{model_name}_meta.json"
    )

    if not os.path.exists(meta_path):

        raise HTTPException(
            404,
            "Model metadata not found"
        )

    with open(meta_path) as f:
        meta = json.load(f)

    # CSV
    if "features" in meta and "target" in meta:

        features = meta["features"]
        target = meta["target"]

        example = {}

        for f in features:

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

    # NC4
    elif meta.get("dataset_type") == "nc4":

        return {
            "model_name": model_name,
            "dataset_type": "nc4",
            "target_variable": meta.get("target_variable"),
            "feature_variables": meta.get("feature_variables"),
            "message": "Upload .nc4 file for prediction"
        }

    # IMAGE
    else:

        return {
            "model_name": model_name,
            "dataset_type": "image",
            "message": "Upload image file for prediction"
        }


# ======================================================
# DATASET DETECTOR
# ======================================================

def detect_dataset(
    csv_files,
    image_files,
    nc4_files
):

    if nc4_files:
        return "nc4"

    if image_files:

        folders = set()

        for path in image_files:
            folders.add(
                os.path.dirname(path)
            )

        if len(folders) > 1:
            return "image_labeled"

        return "image_unlabeled"

    if csv_files:
        return "csv"

    return "unknown"


# ======================================================
# UPLOAD DATASET
# ======================================================

@app.post("/upload-dataset/")
async def upload_dataset(

    file: UploadFile = File(...),

    current_user: dict = Depends(get_current_user)

):

    filename = file.filename.lower()

    # ==================================================
    # USER DATASET FOLDER
    # ==================================================

    user_dataset_dir = os.path.join(
        "datasets",
        f"user_{current_user['id']}"
    )

    os.makedirs(
        user_dataset_dir,
        exist_ok=True
    )

    # ==================================================
    # SAVE ORIGINAL FILE
    # ==================================================

    saved_file_path = os.path.join(
        user_dataset_dir,
        file.filename
    )

    with open(saved_file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # ==================================================
    # FILE SIZE
    # ==================================================

    size_mb = get_file_size_mb(
        saved_file_path
    )

    # ==================================================
    # CSV DATASET
    # ==================================================

    if filename.endswith(".csv"):

        df = pd.read_csv(
            saved_file_path,
            low_memory=False
        )

        # cleaning
        df = df.drop_duplicates()
        df = df.ffill()

        # preview
        preview = (
            df.head(5)
            .replace({np.nan: None})
            .to_dict()
        )

        # summary
        summary = (
            df.describe(include="all")
            .replace({np.nan: None})
            .to_dict()
        )

        # save dataset info in DB
        insert_dataset(
            user_id=current_user["id"],
            dataset_name=file.filename,
            dataset_type="csv",
            file_path=saved_file_path,
            file_size_mb=size_mb
        )

        return {

            "message": "CSV dataset uploaded",

            "dataset_type": "csv",

            "dataset_name": file.filename,

            "rows": int(len(df)),

            "columns": list(df.columns),

            "size_mb": size_mb,

            "preview": preview,

            "summary": summary,

            "saved_path": saved_file_path
        }

    # ==================================================
    # ZIP DATASET
    # ==================================================

    elif filename.endswith(".zip"):

        # ----------------------------------------------
        # Extract dir
        # ----------------------------------------------

        extract_dir = os.path.join(
            user_dataset_dir,
            "extracted"
        )

        shutil.rmtree(
            extract_dir,
            ignore_errors=True
        )

        os.makedirs(
            extract_dir,
            exist_ok=True
        )

        # ----------------------------------------------
        # Extract ZIP
        # ----------------------------------------------

        with zipfile.ZipFile(
            saved_file_path,
            "r"
        ) as zip_ref:

            zip_ref.extractall(extract_dir)

        # ----------------------------------------------
        # Detect contents
        # ----------------------------------------------

        csv_files = []
        image_files = []
        nc4_files = []

        for root, _, files in os.walk(extract_dir):

            for name in files:

                path = os.path.join(root, name)

                if name.lower().endswith(".csv"):
                    csv_files.append(path)

                elif name.lower().endswith(
                    (".jpg", ".jpeg", ".png")
                ):
                    image_files.append(path)

                elif name.lower().endswith(
                    (".nc", ".nc4")
                ):
                    nc4_files.append(path)

        # ----------------------------------------------
        # Detect dataset type
        # ----------------------------------------------

        dataset_type = detect_dataset(
            csv_files,
            image_files,
            nc4_files
        )

        # ----------------------------------------------
        # Save dataset DB
        # ----------------------------------------------

        insert_dataset(
            user_id=current_user["id"],
            dataset_name=file.filename,
            dataset_type=dataset_type,
            file_path=extract_dir,
            file_size_mb=size_mb
        )

        # ----------------------------------------------
        # Result
        # ----------------------------------------------

        result = {

            "message": "ZIP dataset uploaded",

            "dataset_name": file.filename,

            "dataset_type": dataset_type,

            "size_mb": size_mb,

            "csv_files": len(csv_files),

            "images": len(image_files),

            "nc4_files": len(nc4_files),

            "saved_path": extract_dir
        }

        # ----------------------------------------------
        # NC4 variable preview
        # ----------------------------------------------

        if nc4_files:

            try:

                nc_data = Dataset(
                    nc4_files[0]
                )

                variables = list(
                    nc_data.variables.keys()
                )

                nc_data.close()

                result["nc4_variables"] = variables

            except Exception as e:

                result["nc4_error"] = str(e)

        return result

    # ==================================================
    # INVALID FILE
    # ==================================================

    else:

        raise HTTPException(
            status_code=400,
            detail="Only CSV or ZIP files supported"
        )
    

@app.get("/my-datasets")
def my_datasets(

    current_user: dict = Depends(get_current_user)

):

    rows = get_user_datasets(
        current_user["id"]
    )

    return rows


# ======================================================
# FEATURE ENGINEERING
# ======================================================

@app.post("/feature-engineering/")
async def feature_engineering(
    file: UploadFile = File(...),
    target_column: str = Form(None)
):

    filename = file.filename.lower()

    if filename.endswith(".csv"):

        if not target_column:

            raise HTTPException(
                400,
                "target_column required for CSV"
            )

        contents = await file.read()

        df = pd.read_csv(
            StringIO(
                contents.decode("utf-8")
            ),
            low_memory=False
        )

        X, y = smart_preprocessing(
            df,
            target_column
        )

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

        raise HTTPException(
            400,
            "Unsupported file format"
        )


# ======================================================
# TRAIN MODEL
# ======================================================

@app.post("/train-model/")
async def train_model(
    file: UploadFile = File(...),
    target_column: str = Form(None),
    model_name: str = Form("default_model"),
    token: str = Form(...)
):

    from mlops.db import insert_model, get_versioned_model_path

    user = get_current_user(token)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user_id = user["id"]
    user_model_dir = f"{MODEL_DIR}/user_{user_id}"
    os.makedirs(user_model_dir, exist_ok=True)

    filename = file.filename.lower()

    # CSV
    if filename.endswith(".csv"):

        if not target_column:

            raise HTTPException(
                400,
                "target_column required"
            )

        contents = await file.read()

        df = pd.read_csv(
            StringIO(
                contents.decode("utf-8")
            ),
            low_memory=False
        )

        X, y = smart_preprocessing(
            df,
            target_column
        )

        X_train, X_test, y_train, y_test = auto_split(X, y)

        result = train_models(
            X_train,
            X_test,
            y_train,
            y_test,
            features=list(X.columns),
            target=target_column,
            model_name=model_name,
            user_dir=user_model_dir
        )

        # Save to DB
        model_path = f"{user_model_dir}/{model_name}_v1.pkl"
        insert_model(
            user_id=user_id,
            model_name=model_name,
            model_type="csv",
            version=1,
            file_path=model_path
        )

        return {
            "dataset_type": "csv",
            "model_name": model_name,
            "target": target_column,
            "user_id": user_id,
            "training_result": result
        }

    # ZIP
    elif filename.endswith(".zip"):

        zip_path = os.path.join(
            UPLOAD_DIR,
            file.filename
        )

        with open(zip_path, "wb") as f:
            f.write(await file.read())

        shutil.rmtree(
            EXTRACT_DIR,
            ignore_errors=True
        )

        os.makedirs(
            EXTRACT_DIR,
            exist_ok=True
        )

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

                elif name.lower().endswith(
                    (".jpg", ".png", ".jpeg")
                ):
                    image_files.append(path)

                elif name.endswith(".nc4"):
                    nc4_files.append(path)

        dataset_type = detect_dataset(
            csv_files,
            image_files,
            nc4_files
        )

        if dataset_type == "image_labeled":

            result = train_labeled_images(
                EXTRACT_DIR,
                model_name,
                user_dir=user_model_dir
            )

            insert_model(
                user_id=user_id,
                model_name=model_name,
                model_type="image_labeled",
                version=1,
                file_path=f"{user_model_dir}/{model_name}_v1.pkl"
            )

            return {
                "dataset_type": dataset_type,
                "model_name": model_name,
                "user_id": user_id,
                "result": result
            }

        if dataset_type == "image_unlabeled":

            result = cluster_images(
                EXTRACT_DIR,
                model_name,
                user_dir=user_model_dir
            )

            insert_model(
                user_id=user_id,
                model_name=model_name,
                model_type="image_unlabeled",
                version=1,
                file_path=f"{user_model_dir}/{model_name}_v1.pkl"
            )

            return {
                "dataset_type": dataset_type,
                "model_name": model_name,
                "user_id": user_id,
                "result": result
            }

        if dataset_type == "nc4":

            result = analyze_nc4(
                nc4_files[0],
                target_column,
                model_name,
                user_dir=user_model_dir
            )

            insert_model(
                user_id=user_id,
                model_name=model_name,
                model_type="nc4",
                version=1,
                file_path=f"{user_model_dir}/{model_name}_v1.pkl"
            )

            return {
                "dataset_type": dataset_type,
                "model_name": model_name,
                "user_id": user_id,
                "result": result
            }

        return {
            "dataset_type": "unknown"
        }

    else:

        raise HTTPException(
            400,
            "Unsupported file format"
        )


# ======================================================
# PREDICT CSV
# ======================================================

class CSVPrediction(BaseModel):

    model_name: str
    data: dict
    token: str


@app.post("/predict-csv/")
async def predict_csv_api(
    input: CSVPrediction
):

    from mlops.db import get_model_by_name

    log_api("/predict-csv/")

    user = get_current_user(input.token)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    # Check if user owns this model
    model = get_model_by_name(
        user["id"],
        input.model_name
    )

    if not model:
        raise HTTPException(
            status_code=403,
            detail="Model not found or access denied"
        )

    return predict_csv(
        input.model_name,
        input.data,
        user_dir=f"{MODEL_DIR}/user_{user['id']}"
    )


# ======================================================
# PREDICT IMAGE
# ======================================================

@app.post("/predict-image/")
async def predict_image_api(
    model_name: str = Form(...),
    file: UploadFile = File(...),
    token: str = Form(...)
):

    from mlops.db import get_model_by_name

    log_api("/predict-image/")

    user = get_current_user(token)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    # Check if user owns this model
    model = get_model_by_name(
        user["id"],
        model_name
    )

    if not model:
        raise HTTPException(
            status_code=403,
            detail="Model not found or access denied"
        )

    path = f"{UPLOAD_DIR}/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    return predict_image(
        model_name,
        path,
        user_dir=f"{MODEL_DIR}/user_{user['id']}"
    )


# ======================================================
# PREDICT NC4
# ======================================================

@app.post("/predict-nc4/")
async def predict_nc4_api(
    model_name: str = Form(...),
    file: UploadFile = File(...)
):

    log_api("/predict-nc4/")

    path = f"{UPLOAD_DIR}/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    return predict_nc4(
        model_name,
        path
    )