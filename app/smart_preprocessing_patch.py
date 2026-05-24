from .feature_engineering import auto_feature_engineering

# ...existing code...

def smart_preprocessing(df, target_column):
    # DEPRECATED: Use auto_feature_engineering instead
    fe = auto_feature_engineering(df, target_column)
    return fe["X"], fe["y"]
