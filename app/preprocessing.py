import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder


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

    if target_column not in df.columns:
        raise ValueError("Target column not found")

    # remove duplicates
    df = df.drop_duplicates()

    # separate target
    y = df[target_column]
    X = df.drop(columns=[target_column])

    # =============================
    # STEP 1: remove useless columns
    # =============================
    useless_cols = detect_useless_columns(X)
    X = X.drop(columns=useless_cols, errors='ignore')

    # =============================
    # STEP 2: detect column types
    # =============================
    cat_cols = X.select_dtypes(include=["object"]).columns.tolist()
    num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()

    # =============================
    # STEP 3: handle missing values FIRST
    # =============================
    for col in num_cols:
        X[col] = X[col].fillna(X[col].median())

    for col in cat_cols:
        X[col] = X[col].fillna("unknown")

    # =============================
    # STEP 4: smart categorical encoding
    # =============================
    low_card_cols = []
    high_card_cols = []

    for col in cat_cols:
        if X[col].nunique() < 20:
            low_card_cols.append(col)
        else:
            high_card_cols.append(col)

    # One-hot encoding (low cardinality)
    if len(low_card_cols) > 0:
        X = pd.get_dummies(X, columns=low_card_cols, drop_first=True)

    # Label encoding (high cardinality)
    for col in high_card_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))

    # =============================
    # STEP 5: scale numeric features
    # =============================
    scaler = StandardScaler()

    numeric_cols_after = X.select_dtypes(include=["int64", "float64"]).columns

    X[numeric_cols_after] = scaler.fit_transform(X[numeric_cols_after])

    return X, y


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