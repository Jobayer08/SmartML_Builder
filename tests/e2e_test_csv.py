import os
import pandas as pd
from app.feature_engineering import auto_feature_engineering
from app.ml_engine import train_models
from app.predict_engine import predict_csv

# Create small dataframe
csv_path = 'tests/sample_train.csv'
os.makedirs('tests', exist_ok=True)

if not os.path.exists(csv_path):
    df = pd.DataFrame({
        'feature_num': [1.0, 2.0, 3.0, 4.0, 5.0],
        'feature_cat': ['a', 'b', 'a', 'b', 'a'],
        'target': [0, 1, 0, 1, 0]
    })
    df.to_csv(csv_path, index=False)
else:
    df = pd.read_csv(csv_path)

# Feature engineering
fe = auto_feature_engineering(df, 'target')
X = fe['X']
y = fe['y']
preprocessor = fe['preprocessor']

# train/test split
from app.preprocessing import auto_split
X_train, X_test, y_train, y_test = auto_split(X, y)

# Train models (user_dir to simulate per-user save)
user_dir = 'models/user_999'
os.makedirs(user_dir, exist_ok=True)
result = train_models(
    X_train,
    X_test,
    y_train,
    y_test,
    features=list(X.columns),
    target='target',
    model_name='e2e_test_model',
    preprocessor=preprocessor,
    user_dir=user_dir
)

print('Train result:', result)

# Predict using a sample input
input_data = {'feature_num': 2.5, 'feature_cat': 'a'}
resp = predict_csv('e2e_test_model', input_data, user_dir=user_dir)
print('Prediction response:', resp)
