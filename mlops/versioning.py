# mlops/versioning.py

import os
from mlops.db import insert_model

MODEL_DIR = "models"


# ---------------------------------------------------
# 🔍 FIND NEXT VERSION
# ---------------------------------------------------
def get_next_version(model_name, search_dir=None):
    """Find next version number for a model.
    
    Args:
        model_name: Name of the model (without version suffix)
        search_dir: Directory to search in. If None, defaults to MODEL_DIR
    """

    search_path = search_dir or MODEL_DIR

    if not os.path.exists(search_path):
        os.makedirs(search_path)

    versions = []

    for f in os.listdir(search_path):

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
def get_versioned_model_path(model_name, user_dir=None):
    """Generate a versioned model path.
    
    Args:
        model_name: Name of the model
        user_dir: User-specific directory. If provided, path will be in that directory
        
    Returns:
        Tuple of (full_path, version_number)
    """

    if user_dir:
        os.makedirs(user_dir, exist_ok=True)
        version = get_next_version(model_name, search_dir=user_dir)
        filename = f"{model_name}_v{version}.pkl"
        full_path = os.path.join(user_dir, filename)
    else:
        version = get_next_version(model_name)
        filename = f"{model_name}_v{version}.pkl"
        full_path = os.path.join(MODEL_DIR, filename)

    return full_path, version


# ---------------------------------------------------
# 📝 REGISTER MODEL INTO DATABASE
# ---------------------------------------------------
def register_model(model_name, model_type, version, user_id=None, file_path=None):
    """Register model. If `user_id` and `file_path` are provided, insert into DB.
    Otherwise return registration metadata only (useful for system/global models).
    """

    if user_id is not None and file_path is not None:
        try:
            insert_model(
                user_id=user_id,
                model_name=model_name,
                model_type=model_type,
                version=version,
                file_path=file_path
            )
        except Exception:
            # Don't fail registration on DB insert issues; caller can handle logging
            pass

    return {
        "status": "registered",
        "model": model_name,
        "version": version
    }