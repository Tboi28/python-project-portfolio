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

# --- Sample Tariff Rates (Mock Data) ---
tariff_table = {
    "Steel": {2017: 5, 2024: 25},
    "Electronics": {2017: 2, 2024: 10},
    "Automobile Parts": {2017: 3, 2024: 20}
}
tariff_pre = tariff_table[product][2017]
tariff_post = tariff_table[product][2024]

# --- Cost Calculations ---
pre_tariff_total = quantity * unit_cost * (1 + tariff_pre / 100)
post_tariff_total = quantity * unit_cost * (1 + tariff_post / 100)

st.subheader("📦 Cost Comparison")
cost_df = pd.DataFrame({
    "Scenario": ["Pre-Tariff", "Post-Tariff"],
    "Tariff Rate (%)": [tariff_pre, tariff_post],
    "Total Landed Cost (USD)": [pre_tariff_total, post_tariff_total]
})
st.dataframe(cost_df)

# --- Bar Chart ---
fig = go.Figure()
fig.add_trace(go.Bar(x=["Pre-Tariff", "Post-Tariff"], y=[pre_tariff_total, post_tariff_total],
                     name="Total Landed Cost", marker_color=["green", "red"]))
fig.update_layout(title="Total Landed Cost Comparison", yaxis_title="USD")
st.plotly_chart(fig)

# --- Map Visualization ---
st.subheader("🌐 Shipping Route Map")

geolocator = Nominatim(user_agent="tariff_simulator")
try:
    origin_loc = geolocator.geocode(origin)
    dest_loc = geolocator.geocode(destination)

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
    st.plotly_chart(fig_map)

except:
    st.warning("Unable to geocode selected countries. Try different values.")
