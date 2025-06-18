import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from geopy.geocoders import Nominatim

# --- Title ---
st.title("🌍 Tariff Impact Simulator")

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

# --- Safety check for year in data ---
if year in tariff_table[product]:
    selected_tariff = tariff_table[product][year]
else:
    selected_tariff = list(tariff_table[product].values())[-1]

base_tariff = tariff_table[product][2017]  # comparison baseline

# --- Cost Calculations ---
base_cost = quantity * unit_cost * (1 + base_tariff / 100)
year_cost = quantity * unit_cost * (1 + selected_tariff / 100)

# --- Display Cost Comparison ---
st.subheader("📦 Cost Comparison")
cost_df = pd.DataFrame({
    "Scenario": ["Pre-Tariff (2017)", f"Selected Year ({year})"],
    "Tariff Rate (%)": [base_tariff, selected_tariff],
    "Total Landed Cost (USD)": [base_cost, year_cost]
})
st.dataframe(cost_df, use_container_width=True)

# --- Bar Chart ---
fig = go.Figure()
fig.add_trace(go.Bar(
    x=cost_df["Scenario"],
    y=cost_df["Total Landed Cost (USD)"],
    marker_color=["green", "red"]
))
fig.update_layout(title="Total Landed Cost Comparison", yaxis_title="USD")
st.plotly_chart(fig, use_container_width=True)

# --- Map Visualization ---
st.subheader("🌐 Shipping Route Map")
geolocator = Nominatim(user_agent="tariff_simulator")

try:
    origin_loc = geolocator.geocode(origin)
    dest_loc = geolocator.geocode(destination)

    if origin_loc and dest_loc:
        map_df = pd.DataFrame({
            "lat": [origin_loc.latitude, dest_loc.latitude],
            "lon": [origin_loc.longitude, dest_loc.longitude],
            "label": [f"Origin: {origin}", f"Destination: {destination}"]
        })

        fig_map = go.Figure()
        fig_map.add_trace(go.Scattergeo(
            locationmode='country names',
            lon=map_df["lon"],
            lat=map_df["lat"],
            text=map_df["label"],
            mode='markers+text',
            marker=dict(size=10, color="blue")
        ))
        fig_map.add_trace(go.Scattergeo(
            lon=[origin_loc.longitude, dest_loc.longitude],
            lat=[origin_loc.latitude, dest_loc.latitude],
            mode='lines',
            line=dict(width=2, color='red')
        ))
        fig_map.update_layout(
            geo=dict(showland=True),
            title="Origin to Destination Route"
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("Could not geocode one of the selected countries.")

except Exception as e:
    st.error(f"Geolocation error: {e}")

