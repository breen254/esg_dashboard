import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

# Page setup
st.set_page_config(page_title="📊 ESG Trends", layout="wide")

# Custom styling: futuristic + responsive
st.markdown("""
    <style>
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }

    body {
        background-color: #0e1117;
        color: #ffffff;
        font-family: 'Roboto Mono', monospace;
    }

    .fade-in {
        animation: fadeIn ease 1.5s;
        opacity: 0;
        transform: translateY(20px);
        animation-fill-mode: forwards;
    }

    @keyframes fadeIn {
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .floating-nav {
        position: fixed;
        top: 65px;
        left: 20px;
        z-index: 100;
        padding: 12px 20px;
        border-radius: 16px;
        box-shadow: 0 0 20px #00eaff99;
        backdrop-filter: blur(2px);
        font-family: 'Orbitron', sans-serif;
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }

    .floating-nav a {
        color: #00eaff;
        text-decoration: none;
        font-weight: bold;
        font-size: 1.05rem;
        letter-spacing: 1.1px;
        transition: color 0.3s ease, text-shadow 0.3s ease;
    }

    .floating-nav a:hover {
        color: #00fff7;
        text-shadow: 0 0 6px #00fff7;
    }

    h1 {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.5rem;
        color: #00eaff;
        text-shadow: 0 0 8px #00eaff99;
    }

    p.subtitle {
        color: #88ccee;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
    }

    .stSelectbox > label, .stSlider > label, .stMultiSelect > label {
        color: #00eaff;
        font-weight: bold;
        letter-spacing: 0.5px;
    }

    @media screen and (max-width: 768px) {
        .floating-nav {
            top: 65px;
            left: 10px;
            padding: 2px 3px;
            border-radius: 8px;
            box-shadow: 0 0 10px #00eaff99;
            font-size: 0.4rem;
        }

        .floating-nav a {
            display: block;
            margin: 8px 0;
        }

        h1 {
            font-size: 1.8rem;
        }

        p.subtitle {
            font-size: 1rem;
        }
    }
    </style>

    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Roboto+Mono&display=swap" rel="stylesheet">

    <div class="floating-nav fade-in">
        <a href="/" target="_self">🏠 Home</a>
        <a href="/Trends" target="_self">📊 Trends</a>
        <a href="/Forecast" target="_self">🔮 Forecast</a>
    </div>
""", unsafe_allow_html=True)

# Header with animation
st.markdown("""
<div class='fade-in'>
    <h1>📈 ESG Indicator Trends</h1>
    <p class='subtitle'>Visualize historical patterns across key sustainability metrics, powered by intelligent insights.</p>
</div>
""", unsafe_allow_html=True)

# Load and prepare data
df = load_data()
pivot_df = df.pivot_table(index=["Country", "Year"], columns="Indicators", values="Value").reset_index()

# User inputs
with st.container():
    country = st.selectbox("🌍 Select Country", sorted(df["Country"].unique()))
    year_min, year_max = int(df["Year"].min()), int(df["Year"].max())
    year_range = st.slider("📅 Select Year Range", year_min, year_max, (year_min, year_max))

# Filter dataset
filtered = pivot_df[
    (pivot_df["Country"] == country) &
    (pivot_df["Year"] >= year_range[0]) &
    (pivot_df["Year"] <= year_range[1])
]
indicators = filtered.drop(columns=["Country", "Year"]).columns.tolist()
selected = st.multiselect("📌 Choose ESG Indicators", indicators, default=indicators[:3])

# Dynamic charts for each selected indicator
for ind in selected:
    fig = px.line(
        filtered,
        x="Year",
        y=ind,
        title=f"📊 {ind}",
        markers=True,
        template="plotly_dark"
    )
    fig.update_layout(
        title_font_color="#00eaff",
        title_font_size=20,
        margin=dict(t=60, b=40),
        hoverlabel=dict(bgcolor="#222", font_size=12, font_color="#00eaff")
    )
    st.plotly_chart(fig, use_container_width=True)

# Optional footer (consistent styling)
st.markdown("""
<hr style='border-color: #333;'/>
<p style='font-size: 0.85rem; color: #666;'>🛰️ Data visualized using AI-enhanced dashboards. Built for clarity, precision, and sustainability insights.</p>
""", unsafe_allow_html=True)
