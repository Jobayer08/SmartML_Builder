import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def auto_feature_engineering(df):
    df = df.drop_duplicates()
    df = df.ffill()

    cat_cols = df.select_dtypes(include=["object"]).columns
    num_cols = df.select_dtypes(exclude=["object"]).columns

    # One-hot encode categorical columns
    if len(cat_cols) > 0:
        df = pd.get_dummies(df, columns=cat_cols)

    # Scale numeric columns
    if len(num_cols) > 0:
        scaler = StandardScaler()
        df[num_cols] = scaler.fit_transform(df[num_cols])

    return df


def auto_split(df, target_column):
    if target_column not in df.columns:
        raise ValueError("Target column not found in dataset")

    X = df.drop(columns=[target_column])
    y = df[target_column]

    return train_test_split(X, y, test_size=0.2, random_state=42)
