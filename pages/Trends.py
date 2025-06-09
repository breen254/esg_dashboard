import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.set_page_config(page_title="📊 ESG Trends", layout="wide")

mode = st.sidebar.radio("🎨 Theme Mode", ["Dark", "Light"], index=0)
dark_mode = mode == "Dark"

st.markdown(f"""
    <style>
    body {{ background-color: {'#0e1117' if dark_mode else '#ffffff'}; color: {'#ffffff' if dark_mode else '#000000'}; }}
    .fade-in {{ animation: fadeIn ease 2s; }}
    @keyframes fadeIn {{ 0% {{opacity:0;}} 100% {{opacity:1;}} }}
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='fade-in'>
<h1 style='color:#0ff;'>📈 ESG Indicator Trends</h1>
</div>
""", unsafe_allow_html=True)

df = load_data()
country = st.sidebar.selectbox("🌎 Country", sorted(df["Country"].unique()))
year_min, year_max = int(df["Year"].min()), int(df["Year"].max())
year_range = st.sidebar.slider("📅 Year Range", year_min, year_max, (2010, 2020))

pivot_df = df.pivot_table(index=["Country", "Year"], columns="Indicators", values="Value").reset_index()
filtered = pivot_df[(pivot_df["Country"] == country) & (pivot_df["Year"] >= year_range[0]) & (pivot_df["Year"] <= year_range[1])]

indicators = filtered.drop(columns=["Country", "Year"]).columns.tolist()
selected = st.multiselect("Choose indicators", indicators, default=indicators[:3])

for ind in selected:
    fig = px.line(filtered, x="Year", y=ind, title=ind, markers=True, template="plotly_dark" if dark_mode else "plotly")
    st.plotly_chart(fig, use_container_width=True)
