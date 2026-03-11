import numpy as np
import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split, GridSearchCV

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    mean_squared_error
)

from sklearn.preprocessing import LabelEncoder


MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)


# =========================
# Detect ML Problem Type
# =========================
def detect_problem_type(y):

    unique_values = len(np.unique(y))

    if unique_values <= 10:
        return "classification"
    else:
        return "regression"


# =========================
# Data Preparation
# =========================
def prepare_data(df, target):

    if target not in df.columns:
        raise ValueError("Target column not found in dataset")

    X = df.drop(columns=[target])
    y = df[target]

    # Encode categorical columns
    X = pd.get_dummies(X)

    # Encode target if categorical
    if y.dtype == "object":
        encoder = LabelEncoder()
        y = encoder.fit_transform(y)

    return X, y


# =========================
# Hyperparameter Optimization
# =========================
def optimize_model(model, X_train, y_train, problem_type):

    if problem_type == "classification":

        param_grid = {
            "n_estimators": [50, 100],
            "max_depth": [5, 10, None]
        }

        if isinstance(model, RandomForestClassifier):

            grid = GridSearchCV(
                model,
                param_grid,
                cv=3,
                scoring="accuracy"
            )

            grid.fit(X_train, y_train)

            return grid.best_estimator_, grid.best_params_

    return model, {}


# =========================
# Train ML Models
# =========================
def train_models(X_train, X_test, y_train, y_test):

    problem_type = detect_problem_type(y_train)

    results = {}
    trained_models = {}

    # =========================
    # Classification Models
    # =========================
    if problem_type == "classification":

        models = {
            "Logistic Regression": LogisticRegression(max_iter=1000),
            "Decision Tree": DecisionTreeClassifier(),
            "Random Forest": RandomForestClassifier()
        }

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

            trained_models[name] = model

        best_model_name = max(results, key=lambda x: results[x]["accuracy"])
        best_model = trained_models[best_model_name]

    # =========================
    # Regression Models
    # =========================
    else:

        models = {
            "Linear Regression": LinearRegression()
        }

        for name, model in models.items():

            model.fit(X_train, y_train)

            preds = model.predict(X_test)

            rmse = np.sqrt(mean_squared_error(y_test, preds))

            results[name] = {
                "RMSE": float(rmse)
            }

            trained_models[name] = model

        best_model_name = min(results, key=lambda x: results[x]["RMSE"])
        best_model = trained_models[best_model_name]

    # =========================
    # Optimization
    # =========================
    optimized_model, best_params = optimize_model(
        best_model,
        X_train,
        y_train,
        problem_type
    )

    # =========================
    # Save Model
    # =========================
    model_path = os.path.join(MODEL_DIR, "best_csv_model.pkl")

    joblib.dump(optimized_model, model_path)

    return {
        "problem_type": problem_type,
        "model_results": results,
        "best_model": best_model_name,
        "optimization": {
            "best_params": best_params,
            "model_saved_path": model_path
        }
    }


# =========================
# Main CSV Training Pipeline
# =========================
def train_csv_model(df, target):

    X, y = prepare_data(df, target)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    results = train_models(
        X_train,
        X_test,
        y_train,
        y_test
    )

    return results