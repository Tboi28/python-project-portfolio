import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# App title
st.title("💱 USD Exchange Rate Tracker (Last 90 Days)")

# Currency options
currencies = {
    "Euro (EUR)": "EUR",
    "British Pound (GBP)": "GBP",
    "Japanese Yen (JPY)": "JPY",
    "Australian Dollar (AUD)": "AUD",
    "Canadian Dollar (CAD)": "CAD"
}

# Dropdown selector
selected_currency_name = st.selectbox("Choose target currency:", list(currencies.keys()))
target_currency = currencies[selected_currency_name]

# API settings
base_currency = "USD"
days_back = 90
end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=days_back)).strftime('%Y-%m-%d')

# Fetch data
url = f"https://api.frankfurter.app/{start_date}..{end_date}"
params = {"from": base_currency, "to": target_currency}
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    rates = data.get("rates", {})
    df = pd.DataFrame.from_dict(rates, orient="index")
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)

    # Plot
    st.subheader(f"{base_currency} → {target_currency} Exchange Rate (Last 90 Days)")
    st.line_chart(df[target_currency])
else:
    st.error("Failed to fetch exchange rate data.")
