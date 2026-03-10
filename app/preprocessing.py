import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def auto_feature_engineering(df, target_column):
    """
    Perform automatic data cleaning and feature engineering.
    """

    # Check target column
    if target_column not in df.columns:
        raise ValueError("Target column not found in dataset")

    # Remove duplicates
    df = df.drop_duplicates()

    # Fill missing values
    df = df.ffill()

    # Separate features and target
    y = df[target_column]
    X = df.drop(columns=[target_column])

    # Detect column types
    cat_cols = X.select_dtypes(include=["object"]).columns
    num_cols = X.select_dtypes(exclude=["object"]).columns

    # Encode categorical columns
    if len(cat_cols) > 0:
        X = pd.get_dummies(X, columns=cat_cols)

    # Scale numeric columns
    if len(num_cols) > 0:
        scaler = StandardScaler()
        X[num_cols] = scaler.fit_transform(X[num_cols])

    return X, y


def auto_split(X, y):
    """
    Split dataset into train and test sets
    """

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    return X_train, X_test, y_train, y_test