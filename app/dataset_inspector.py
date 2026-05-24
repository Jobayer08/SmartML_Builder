import math
import numpy as np
import pandas as pd

from netCDF4 import Dataset


# =====================================================
# CSV INSPECT
# =====================================================

def _sanitize_value(value):
    if pd.isna(value):
        return None

    if isinstance(value, (np.integer, np.floating, np.bool_)):
        value = value.item()

    if isinstance(value, float):
        if not math.isfinite(value):
            return None

    return value


def inspect_csv(file_path):

    df = pd.read_csv(file_path)

    sample_rows = []
    for _, row in df.head(5).iterrows():
        record = {
            col: _sanitize_value(val)
            for col, val in row.items()
        }
        sample_rows.append(record)

    return {
        "type": "csv",
        "columns": [str(c) for c in df.columns.tolist()],
        "shape": [int(df.shape[0]), int(df.shape[1])],
        "sample_rows": sample_rows
    }


# =====================================================
# NC4 INSPECT
# =====================================================

def inspect_nc4(file_path):

    ds = Dataset(file_path)

    variables = {}

    for var in ds.variables:

        v = ds.variables[var]

        variables[var] = {

            "shape": str(v.shape),

            "dtype": str(v.dtype),

            "units": getattr(
                v,
                "units",
                "unknown"
            )
        }

    ds.close()

    return {

        "type": "nc4",

        "variables": variables
    }