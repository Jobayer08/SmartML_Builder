import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split

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

        best_model = max(results, key=lambda x: results[x]["accuracy"])

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

        best_model = min(results, key=lambda x: results[x]["RMSE"])

    return {
        "problem_type": problem_type,
        "model_results": results,
        "best_model": best_model,
    
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