from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

MODEL_DIR = "models"

os.makedirs(MODEL_DIR, exist_ok=True)

def optimize_model(X_train, y_train):

    param_grid = {
        "n_estimators": [50,100],
        "max_depth": [5,10,None]
    }

    model = RandomForestClassifier()

    grid = GridSearchCV(
        model,
        param_grid,
        cv=3,
        scoring="accuracy"
    )

    grid.fit(X_train,y_train)

    best_model = grid.best_estimator_

    model_path = f"{MODEL_DIR}/best_csv_model.pkl"

    joblib.dump(best_model,model_path)

    return {
        "best_params": grid.best_params_,
        "model_saved": model_path
    }