from fastapi import FastAPI, File, UploadFile
import pandas as pd
from io import StringIO

app = FastAPI()

@app.get("/")
def root():
    return {"status": "SmartML Builder Step 1 Running"}

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(StringIO(contents.decode()))

    # Remove duplicates
    df = df.drop_duplicates()

    # Handle missing values
    df = df.ffill()


    preview = df.head(5).to_dict()
    summary = df.describe(include="all").to_dict()

    return {
        "rows": len(df),
        "columns": list(df.columns),
        "preview": preview,
        "summary": summary
    }
