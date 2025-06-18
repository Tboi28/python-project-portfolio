import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Tariff Impact Simulator",
    layout="centered"
)

# --- Title & Banner ---
st.title("🌍 Tariff Impact Simulator")

# --- Dependency Safety Block ---
try:
    import pandas as pd
    import plotly.graph_objects as go
    from geopy.geocoders import Nominatim
except ModuleNotFoundError as e:
    st.warning("⚠️ This app requires additional Python packages to work.")
    st.error(f"Missing module: `{e.name}`")
    st.markdown("Please make sure your `requirements.txt` includes:")
    st.code("streamlit\npandas\nplotly\ngeopy", language="bash")
    st.stop()

# --- Sidebar Inputs ---
st.sidebar.header("Shipping Inputs")
origin = st.sidebar.selectbox("Origin Country", ["China", "Germany", "Mexico"])
destination = st.sidebar.selectbox("Destination Country", ["USA", "Canada", "UK"])
product = st.sidebar.selectbox("Product Category", ["Steel", "Electronics", "Automobile Parts"])
quantity = st.sidebar.number_input("Quantity", min_value=1, value=100)
unit_cost = st.sidebar.number_input("Unit Cost (USD)", min_value=0.01, value=10.0)
mode = st.sidebar.selectbox("Shipping Mode", ["Ocean", "Air", "Rail"])
year = st.sidebar.select_slider("Simulation Year", options=[2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024])

# --- Tariff Rates (mock data) ---
tariff_table = {
    "Steel": {2017: 5, 2024: 25},
    "Electronics": {2017: 2, 2024: 10},
    "Automobile Parts": {2017: 3, 2024: 20}
}

# --- Simulation Trigger ---
st.subheader("Run Your Tariff Simulation")
if st.button("Run Simulation"):

    if year in tariff_table[product]:
        selected_tariff = tariff_table[product][year]
    else:
        selected_tariff = list(tariff_table[product].value
