import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# =====================================================
# AUTO FEATURE ENGINEERING
# =====================================================
def auto_feature_engineering(df, target_column):
    # -----------------------------------------
    # Split X and y
    # -----------------------------------------
    X = df.drop(columns=[target_column])
    y = df[target_column]

    # -----------------------------------------
    # Detect column types
    # -----------------------------------------
    numeric_features = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_features = X.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

    # -----------------------------------------
    # Numeric pipeline
    # -----------------------------------------
    numeric_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="mean")),
        ("scaler", StandardScaler())
    ])

    # -----------------------------------------
    # Categorical pipeline
    # -----------------------------------------
    categorical_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    # -----------------------------------------
    # Combine preprocessors
    # -----------------------------------------
    preprocessor = ColumnTransformer([
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ])

    # -----------------------------------------
    # Fit transform
    # -----------------------------------------
    X_processed = preprocessor.fit_transform(X)

    # Try to get feature names for the transformed output
    try:
        # sklearn >=1.0
        feature_names = preprocessor.get_feature_names_out(X.columns)
    except Exception:
        # Fallback: combine numeric and categorical feature names
        feature_names = numeric_features + categorical_features

    # Convert to DataFrame for downstream compatibility
    import scipy.sparse as sp

    if sp.issparse(X_processed):
        X_arr = X_processed.toarray()
    else:
        X_arr = X_processed

    X_df = pd.DataFrame(X_arr, columns=feature_names)

    return {
        "X": X_df,
        "y": y,
        "preprocessor": preprocessor,
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
        "feature_names": feature_names.tolist() if hasattr(feature_names, "tolist") else list(feature_names)
    }
