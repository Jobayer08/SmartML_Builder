import os


def detect_dataset_type(filename):

    filename = filename.lower()

    # CSV
    if filename.endswith(".csv"):
        return "csv"

    # IMAGE
    elif filename.endswith((
        ".jpg",
        ".jpeg",
        ".png"
    )):
        return "image"

    # NC4
    elif filename.endswith(".nc"):
        return "nc4"

    return "unknown"


def get_file_size_mb(file_path):

    size = os.path.getsize(file_path)

    return round(size / (1024 * 1024), 2)