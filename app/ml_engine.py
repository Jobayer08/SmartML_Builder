import numpy as np
import joblib
import os
import json

from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    mean_squared_error
)

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)


# -------------------------
# Problem Type Detection
# -------------------------
def detect_problem_type(y):
    return "classification" if len(np.unique(y)) <= 10 else "regression"


# -------------------------
# Save Model + Metadata
# -------------------------
def save_model(model, features, target, model_name):
    joblib.dump(model, f"{MODEL_DIR}/{model_name}.pkl")

    meta = {
        "features": features,
        "target": target
    }

    with open(f"{MODEL_DIR}/{model_name}_meta.json", "w") as f:
        json.dump(meta, f)


# -------------------------
# Hyperparameter Optimization
# -------------------------
def optimize_rf_classifier(model, X, y):
    """Optimize Random Forest for classification"""
    grid = GridSearchCV(
        model,
        {
            "n_estimators": [50, 100, 150],
            "max_depth": [5, 10, 15, None],
            "min_samples_split": [2, 5, 10]
        },
        cv=3,
        scoring="accuracy",
        n_jobs=-1
    )
    grid.fit(X, y)
    return grid.best_estimator_, grid.best_params_


# -------------------------
# Train Models (MAIN)
# -------------------------
def train_models(X_train, X_test, y_train, y_test, features, target, model_name):

    problem_type = detect_problem_type(y_train)
    results = {}

    # ========== CLASSIFICATION ==========
    if problem_type == "classification":

        models = {
            "Logistic Regression": LogisticRegression(max_iter=1000),
            "Decision Tree": DecisionTreeClassifier(),
            "Random Forest": RandomForestClassifier()
        }

        best_acc = 0
        best_model = None
        best_name = ""

        for name, model in models.items():
            model.fit(X_train, y_train)
            preds = model.predict(X_test)

            acc = accuracy_score(y_test, preds)
            prec = precision_score(y_test, preds, average="weighted", zero_division=0)
            rec = recall_score(y_test, preds, average="weighted", zero_division=0)

            results[name] = {
                "accuracy": float(acc),
                "precision": float(prec),
                "recall": float(rec)
            }

            if acc > best_acc:
                best_acc = acc
                best_model = model
                best_name = name

        # Optimize RandomForest only
        if best_name == "Random Forest":
            best_model, best_params = optimize_rf_classifier(best_model, X_train, y_train)
        else:
            best_params = {}

    # ========== REGRESSION ==========
    else:
        best_model = LinearRegression()
        best_model.fit(X_train, y_train)
        preds = best_model.predict(X_test)

        rmse = np.sqrt(mean_squared_error(y_test, preds))

        results["Linear Regression"] = {"RMSE": float(rmse)}
        best_name = "Linear Regression"
        best_params = {}

    # ========== SAVE ==========
    save_model(best_model, features, target, model_name)

    return {
        "problem_type": problem_type,
        "model_results": results,
        "best_model": best_name,
        "optimization": {
            "best_params": best_params,
            "saved_as": model_name
        }
    }