import pandas as pd

from netCDF4 import Dataset


# =====================================================
# CSV INSPECT
# =====================================================

def inspect_csv(file_path):

    df = pd.read_csv(file_path)

    return {

        "type": "csv",

        "columns": df.columns.tolist(),

        "shape": list(df.shape),

        "sample_rows": df.head(5).to_dict(
            orient="records"
        )
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