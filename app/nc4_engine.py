from netCDF4 import Dataset
import numpy as np
import joblib
import os
import json


# =============================
# Model directory
# =============================
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)


def analyze_nc4(file_path, target_variable=None, model_name="nc4_model"):

    # =============================
    # Open NetCDF dataset
    # =============================
    data = Dataset(file_path, "r")

    variables = list(data.variables.keys())
    dimensions = list(data.dimensions.keys())

    # =============================
    # Step 1 — Determine Target Variable
    # =============================
    var_name = None

    # User provided variable
    if target_variable:

        if target_variable not in variables:

            data.close()

            return {
                "error": f"'{target_variable}' not found in dataset",
                "available_variables": variables
            }

        var_name = target_variable

    else:
        # Auto detect usable variable
        for v in variables:

            try:

                values = data.variables[v][:]

                values = np.array(values)

                if values.size == 0:
                    continue

                if np.isnan(values).all():
                    continue

                var_name = v
                break

            except:
                continue

    # =============================
    # If no usable variable found
    # =============================
    if var_name is None:

        data.close()

        return {
            "error": "No valid variable found in NC4 file",
            "available_variables": variables
        }

    # =============================
    # Step 2 — Extract Variable Data
    # =============================
    try:

        values = data.variables[var_name][:]

        values = np.array(values)

        values = values.flatten()

        values = values[~np.isnan(values)]

    except Exception as e:

        data.close()

        return {
            "error": f"Failed to read variable '{var_name}'",
            "details": str(e)
        }

    if len(values) == 0:

        data.close()

        return {
            "error": "Variable contains no usable numeric data",
            "target_variable": var_name
        }

    # =============================
    # Step 3 — Compute Statistics
    # =============================
    mean_val = float(np.mean(values))
    std_val = float(np.std(values))
    min_val = float(np.min(values))
    max_val = float(np.max(values))

    # =============================
    # Step 4 — Save Model
    # =============================
    model_data = {
        "target_variable": var_name,
        "mean": mean_val,
        "std": std_val,
        "min": min_val,
        "max": max_val
    }

    model_path = os.path.join(MODEL_DIR, f"{model_name}.pkl")

    joblib.dump(model_data, model_path)

    # =============================
    # Save Metadata (important for multi-model)
    # =============================
    metadata = {
        "model_name": model_name,
        "dataset_type": "nc4",
        "target_variable": var_name,
        "variables": variables,
        "dimensions": dimensions
    }

    meta_path = os.path.join(MODEL_DIR, f"{model_name}_meta.json")

    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=4)

    data.close()

    # =============================
    # Step 5 — Return Results
    # =============================
    return {

        "dataset_type": "nc4_scientific",

        "model_name": model_name,

        "target_variable": var_name,

        "all_variables": variables,

        "dimensions": dimensions,

        "data_points": int(len(values)),

        "statistics": {
            "mean": mean_val,
            "std": std_val,
            "min": min_val,
            "max": max_val
        },

        "model_saved": model_path,

        "metadata_saved": meta_path
    }