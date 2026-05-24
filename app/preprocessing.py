import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from .feature_engineering import auto_feature_engineering


# =============================
# Detect useless columns
# =============================
def detect_useless_columns(df):
    """
    Identify columns that don't contribute to modeling:
    - ID-like columns (almost unique values)
    - Constant columns (single unique value)
    - Columns with excessive missing data (>70%)
    """
    useless = []

    for col in df.columns:
        unique_ratio = df[col].nunique() / len(df) if len(df) > 0 else 0

        # 1. ID-like column (almost unique)
        if unique_ratio > 0.95:
            useless.append(col)

        # 2. Constant column (no variance)
        elif df[col].nunique() <= 1:
            useless.append(col)

        # 3. Too many missing values
        elif df[col].isnull().mean() > 0.7:
            useless.append(col)

    return useless


# =============================
# SMART PREPROCESSING
# =============================
def smart_preprocessing(df, target_column):
    """Deprecated wrapper: delegate to auto_feature_engineering and
    return (X, y) where X is a DataFrame with feature columns.
    """
    fe = auto_feature_engineering(df, target_column)
    return fe["X"], fe["y"]


# =============================
# TRAIN TEST SPLIT
# =============================
def auto_split(X, y):

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    return X_train, X_test, y_train, y_test