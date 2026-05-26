# app/nc4_engine.py

from netCDF4 import Dataset
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import os
import json

from mlops.versioning import get_versioned_model_path, register_model

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)


# =============================
# 🔍 STEP 0 — INSPECT FUNCTION
# =============================
def inspect_nc4(file_path):

    ds = Dataset(file_path)

    info = {}

    for var in ds.variables:
        v = ds.variables[var]

        info[var] = {
            "shape": v.shape,
            "dtype": str(v.dtype),
            "units": getattr(v, "units", "unknown")
        }

    ds.close()
    return info


# =============================
# Check valid numeric variable
# =============================
def _is_valid_numeric(arr):
    try:
        arr = np.array(arr)
        return arr.size > 0 and not np.isnan(arr).all()
    except:
        return False


# =============================
# Convert NC4 variable → 1D feature
# =============================
def extract_feature(var_data):

    arr = np.array(var_data)

    # multi-dim → mean reduce
    if arr.ndim >= 2:
        return arr.mean(axis=tuple(range(1, arr.ndim)))

    return arr


# =============================
# 🧠 SMART TRAIN FUNCTION
# =============================
def analyze_nc4(file_path, target_variable=None, model_name="nc4_model", user_dir=None):

    ds = Dataset(file_path, "r")

    variables = list(ds.variables.keys())
    dimensions = list(ds.dimensions.keys())

    # =============================
    # STEP 1 — AUTO / MANUAL TARGET
    # =============================
    if target_variable:

        if target_variable not in variables:
            ds.close()
            return {
                "error": f"{target_variable} not found",
                "available_variables": variables
            }

        target_var = target_variable

    else:
        # auto pick first numeric
        target_var = None

        for v in variables:
            if _is_valid_numeric(ds.variables[v][:]):
                target_var = v
                break

        if target_var is None:
            ds.close()
            return {"error": "No usable variable found"}

    # =============================
    # STEP 2 — TARGET PREP
    # =============================
    y_raw = ds.variables[target_var][:]
    y = extract_feature(y_raw)

    if len(np.shape(y)) == 0:
        ds.close()
        return {"error": "Target variable invalid"}

    target_len = len(y)

    # =============================
    # STEP 3 — FEATURE BUILD
    # =============================
    X_list = []
    feature_names = []

    for v in variables:

        if v == target_var:
            continue

        try:
            data = ds.variables[v][:]

            if not _is_valid_numeric(data):
                continue

            feat = extract_feature(data)

            if np.isscalar(feat):
                continue

            feat = np.array(feat)
            if feat.size == 0:
                continue

            X_list.append(feat)
            feature_names.append(v)

        except:
            continue

    if len(X_list) == 0:
        ds.close()
        return {"error": "No feature variables found"}

    common_length = min([target_len] + [len(feat) for feat in X_list])
    if common_length == 0:
        ds.close()
        return {"error": "No usable samples found"}

    y = y[:common_length]
    X = np.vstack([feat[:common_length] for feat in X_list]).T

    # =============================
    # STEP 5 — TRAIN MODEL
    # =============================
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X, y)

    ds_meta = Dataset(file_path)

    units = {}
    for var in variables:
        units[var] = getattr(ds_meta.variables[var], "units", "unknown")

    ds_meta.close()

    # =============================
    # STEP 7 — SAVE MODEL (🔥 IMPORTANT CHANGE)
    # =============================
    model_data = {
        "model": model,
        "target": target_var,
        "features": feature_names,
        "units": units,
        "dimensions": dimensions
    }

    if user_dir:
        os.makedirs(user_dir, exist_ok=True)
        version = 1
        model_path = os.path.join(user_dir, f"{model_name}_v{version}.pkl")
    else:
        model_path, version = get_versioned_model_path(f"{model_name}_nc4")
    joblib.dump(model_data, model_path)

    register_model(
        model_name=model_name,
        model_type="nc4",
        version=version
    )

    # =============================
    # STEP 8 — OPTIONAL JSON META
    # =============================
    meta = {
        "model_name": model_name,
        "target": target_var,
        "features": feature_names,
        "samples": int(len(y)),
        "units": units
    }

    meta_path = os.path.join(MODEL_DIR, f"{model_name}_meta.json")

    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=4)

    # =============================
    # STEP 9 — RETURN
    # =============================
    return {
        "dataset_type": "nc4_ml",
        "model_name": model_name,
        "target": target_var,
        "target_unit": units.get(target_var, "unknown"),
        "features": feature_names,
        "feature_units": {f: units.get(f, "unknown") for f in feature_names},
        "samples": int(len(y)),
        "model_saved": model_path,
        "version": version,
        "status": "NC4 smart training completed ✅"
    }