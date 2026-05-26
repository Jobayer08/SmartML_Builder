# mlops/logger.py

from mlops.db import (
    insert_prediction,
    insert_api_usage
)


# ---------------------------------------------------
# 📦 LOG PREDICTION
# ---------------------------------------------------
def log_prediction(model_name, input_type, prediction, user_id=None):

    try:

        insert_prediction(
            user_id=user_id,
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
def log_api(endpoint, user_id=None):

    try:

        insert_api_usage(endpoint, user_id=user_id)

        return {
            "status": "logged"
        }

    except Exception as e:

        return {
            "status": "failed",
            "error": str(e)
        }