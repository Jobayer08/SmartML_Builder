# mlops/logger.py

from mlops.db import (
    insert_prediction,
    insert_api_usage
)


# ---------------------------------------------------
# 📦 LOG PREDICTION
# ---------------------------------------------------
def log_prediction(model_name, input_type, prediction):

    try:

        insert_prediction(
            model_name=model_name,
            input_type=input_type,
            prediction=prediction
        )

        return {
            "status": "logged"
        }

    except Exception as e:

        return {
            "status": "failed",
            "error": str(e)
        }


# ---------------------------------------------------
# 🌐 LOG API USAGE
# ---------------------------------------------------
def log_api(endpoint):

    try:

        insert_api_usage(endpoint)

        return {
            "status": "logged"
        }

    except Exception as e:

        return {
            "status": "failed",
            "error": str(e)
        }