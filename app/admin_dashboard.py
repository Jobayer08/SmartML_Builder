import streamlit as st
import pandas as pd
from sqlalchemy import text, create_engine

# Database connection
DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/smartml"
engine = create_engine(DATABASE_URL)

st.set_page_config(
    page_title="SmartML Admin Panel",
    layout="wide"
)

st.title("🚀 SmartML Builder Admin Dashboard")

# ======================================================
# TOTAL MODELS
# ======================================================

with engine.connect() as conn:

    model_count = conn.execute(
        text("SELECT COUNT(DISTINCT model_name) FROM models")
    ).scalar()

    prediction_count = conn.execute(
        text("SELECT COUNT(*) FROM predictions")
    ).scalar()

    top_model = conn.execute(text("""
        SELECT model_name, COUNT(*) as total
        FROM predictions
        GROUP BY model_name
        ORDER BY total DESC
        LIMIT 1
    """)).fetchone()

col1, col2, col3 = st.columns(3)

col1.metric("📦 Total Models", model_count)
col2.metric("🔮 Total Predictions", prediction_count)

if top_model:
    col3.metric(
        "🔥 Most Used Model",
        f"{top_model[0]} ({top_model[1]})"
    )

# ======================================================
# PREDICTION TYPE DISTRIBUTION
# ======================================================

st.subheader("📊 Prediction Type Usage")

with engine.connect() as conn:

    rows = conn.execute(text("""
        SELECT input_type, COUNT(*) as total
        FROM predictions
        GROUP BY input_type
    """)).fetchall()

if rows:

    df = pd.DataFrame(rows, columns=["Type", "Count"])

    st.bar_chart(
        df.set_index("Type")
    )

# ======================================================
# MODEL VERSION TABLE
# ======================================================

st.subheader("🧠 Model Versions")

with engine.connect() as conn:

    rows = conn.execute(text("""
        SELECT model_name, version, created_at
        FROM models
        ORDER BY created_at DESC
    """)).fetchall()

if rows:

    df = pd.DataFrame(
        rows,
        columns=["Model", "Version", "Created At"]
    )

    st.dataframe(df, use_container_width=True)

# ======================================================
# PREDICTION LOGS
# ======================================================

st.subheader("📜 Prediction Logs")

with engine.connect() as conn:

    rows = conn.execute(text("""
        SELECT model_name,
               input_type,
               prediction,
               created_at
        FROM predictions
        ORDER BY created_at DESC
        LIMIT 100
    """)).fetchall()

if rows:

    df = pd.DataFrame(
        rows,
        columns=[
            "Model",
            "Type",
            "Prediction",
            "Time"
        ]
    )

    st.dataframe(df, use_container_width=True)

st.success("✅ SmartML Builder MLOps Dashboard Running")