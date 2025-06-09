import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from utils import load_data

st.set_page_config(page_title="🔮 Forecast", layout="wide")

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
<h1 style='color:#0ff;'>🔮 ESG Forecasting</h1>
</div>
""", unsafe_allow_html=True)

df = load_data()
pivot_df = df.pivot_table(index=["Country", "Year"], columns="Indicators", values="Value").reset_index()
target = "Control of Corruption: Estimate"
pivot_df = pivot_df.dropna(subset=[target])

X = pivot_df.drop(columns=["Country", "Year", target])
imputer = SimpleImputer()
X_imputed = imputer.fit_transform(X)
y = pivot_df[target]

X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

country = st.sidebar.selectbox("Select Country", sorted(pivot_df["Country"].unique()))
year_range = st.sidebar.slider("Select Years", int(pivot_df["Year"].min()), int(pivot_df["Year"].max()), (2010, 2020))

filtered = pivot_df[(pivot_df["Country"] == country) & (pivot_df["Year"] >= year_range[0]) & (pivot_df["Year"] <= year_range[1])]
X_input = imputer.transform(filtered.drop(columns=["Country", "Year", target]))
predictions = model.predict(X_input)

results = filtered[["Year", target]].copy()
results["Predicted"] = predictions

st.metric("Latest Actual", f"{results[target].iloc[-1]:.2f}")
st.metric("Latest Prediction", f"{results['Predicted'].iloc[-1]:.2f}")

fig = go.Figure()
fig.add_trace(go.Scatter(x=results["Year"], y=results[target], name="Actual", mode="lines+markers"))
fig.add_trace(go.Scatter(x=results["Year"], y=results["Predicted"], name="Predicted", mode="lines+markers"))
fig.update_layout(title="Actual vs Predicted", template="plotly_dark" if dark_mode else "plotly")
st.plotly_chart(fig, use_container_width=True)
