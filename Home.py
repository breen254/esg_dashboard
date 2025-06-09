import streamlit as st

# Set page configuration
st.set_page_config(page_title="🌐 ESG Dashboard", layout="wide")

# Sidebar theme toggle
mode = st.sidebar.radio("Theme", ["Dark", "Light"])
dark_mode = mode == "Dark"

# Apply custom styles based on theme
st.markdown(f"""
    <style>
    body {{
        background-color: {'#0e1117' if dark_mode else '#ffffff'};
        color: {'#ffffff' if dark_mode else '#000000'};
    }}
    .fade-in {{
        animation: fadeIn ease 2s;
    }}
    @keyframes fadeIn {{
        0% {{opacity:0;}}
        100% {{opacity:1;}}
    }}
    a.dashboard-link {{
        display: inline-block;
        padding: 1rem 2rem;
        margin: 1rem 1rem 0 0;
        border-radius: 12px;
        background-color: {'#1f77b4' if dark_mode else '#e0f7fa'};
        color: {'#fff' if dark_mode else '#000'};
        font-weight: bold;
        text-decoration: none;
        transition: transform 0.3s ease, background-color 0.3s ease;
    }}
    a.dashboard-link:hover {{
        transform: scale(1.05);
        background-color: {'#3399ff' if dark_mode else '#b2ebf2'};
    }}
    </style>
""", unsafe_allow_html=True)

# Animated header
st.markdown("""
<div class='fade-in'>
    <h1 style='color:#0ff; text-shadow:0 0 2px #0ff;'>🌍 Welcome to ESG Forecast Dashboard</h1>
    <p style='color:#aaa;'>Navigate between AI-powered forecasting tools and data trends.</p>
</div>
""", unsafe_allow_html=True)

# Navigation links
st.markdown("""
<div class='fade-in'>
    <a href='/Trends' target='_self' class='dashboard-link'>📊 ESG Trends</a>
    <a href='/Forecast' target='_self' class='dashboard-link'>🔮 ESG Forecast</a>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<h4>🚀 Built by Bkn</h4>", unsafe_allow_html=True)
