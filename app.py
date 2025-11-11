
"""
Streamlit Dashboard (personalized for vidhun mohan)
Auto-detects key columns based on the dataset provided.
Run: streamlit run app.py
"""
import os
import pandas as pd
import streamlit as st
import plotly.express as px

DATA_FILE = "DataCoSupplyChainDataset.csv"

st.set_page_config(layout="wide", page_title="Supply Chain Dashboard - vidhun mohan")
st.title("Supply Chain Analytics — Assignment 1 (vidhun mohan)")

@st.cache_data
def load_data(nrows=None):
    if not os.path.exists(DATA_FILE):
        st.error(f"Dataset file '{DATA_FILE}' not found. Please upload it via the sidebar or place it in the app folder.")
        return None
    return pd.read_csv(DATA_FILE, encoding='ISO-8859-1', low_memory=False, nrows=nrows)

df = None
uploaded = st.sidebar.file_uploader("Upload CSV (optional)", type=["csv"])
if uploaded is not None:
    df = pd.read_csv(uploaded, encoding='ISO-8859-1', low_memory=False)
else:
    df = load_data()

if df is None:
    st.stop()

st.sidebar.header("Columns detected")
cols = df.columns.tolist()
st.sidebar.text("\n".join(map(str, cols[:200])))


# detected columns (best-effort)
sales_col = "Sales per customer"
profit_col = "Order Item Profit Ratio"
category_col = "Category Name"
late_col = "Late_delivery_risk"
ship_days_col = "Days for shipping (real)"
lat_col = "Latitude"
lon_col = "Longitude"

st.header("Dataset snapshot")
st.text(df.head(20).to_string(index=False))

st.header("Top categories by Sales")
if category_col in df.columns and sales_col in df.columns:
    grp = df.groupby(category_col)[sales_col].sum().reset_index().sort_values(by=sales_col, ascending=False).head(10)
    fig = px.bar(grp, x=category_col, y=sales_col, title="Top categories by sales")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Category/Sales columns not found automatically. Inspect columns in the sidebar.")

st.header("Shipping days vs late delivery risk")
if ship_days_col in df.columns and late_col in df.columns:
    sample = df[[ship_days_col, late_col]].dropna().sample(min(20000, len(df)))
    fig2 = px.scatter(sample, x=ship_days_col, y=late_col, title="Ship days vs late delivery risk")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Shipping days or late delivery column not found automatically.")

st.header("Geographic profit scatter (if lat/lon present)")
if lat_col in df.columns and lon_col in df.columns and profit_col in df.columns:
    sample = df[[lon_col, lat_col, profit_col]].dropna().sample(min(10000, len(df)))
    fig3 = px.scatter_mapbox(sample, lat=lat_col, lon=lon_col, color=profit_col, zoom=1, height=600)
    fig3.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("Latitude/Longitude/Profit columns not detected.")

st.markdown("Prepared for: vidhun mohan — Advanced Business Statistics")
