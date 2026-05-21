# mlops/versioning.py

import os
from mlops.db import insert_model

MODEL_DIR = "models"


# ---------------------------------------------------
# 🔍 FIND NEXT VERSION
# ---------------------------------------------------
def get_next_version(model_name):

    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    versions = []

    for f in os.listdir(MODEL_DIR):

        # example:
        # titanic_v1.pkl
        # titanic_v2.pkl

        if f.startswith(model_name + "_v") and f.endswith(".pkl"):

            try:
                version = int(
                    f.replace(".pkl", "").split("_v")[-1]
                )

                versions.append(version)

            except:
                continue

    # no previous version
    if len(versions) == 0:
        return 1

    return max(versions) + 1


# ---------------------------------------------------
# 💾 GENERATE VERSIONED MODEL PATH
# ---------------------------------------------------
def get_versioned_model_path(model_name):

    version = get_next_version(model_name)

    filename = f"{model_name}_v{version}.pkl"

    full_path = os.path.join(MODEL_DIR, filename)

    return full_path, version


# ---------------------------------------------------
# 📝 REGISTER MODEL INTO DATABASE
# ---------------------------------------------------
def register_model(model_name, model_type, version):

    insert_model(
        model_name=model_name,
        model_type=model_type,
        version=version
    )

    return {
        "status": "registered",
        "model": model_name,
        "version": version
    }