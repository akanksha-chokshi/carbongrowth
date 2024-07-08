import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("Carbon Growth Estimation")

country = st.selectbox("Select a Country", ["Philippines"])
forest = st.selectbox("Select Forest Type", ["Terrestrial Forests", "Mangroves"])

values = {
    "Philippines": {
        "Terrestrial Forests": {
            "A": 861.7968,
            "k": 0.0742,
            "m": 2.5737
        },
        "Mangroves": {
            "A": 1286.7245,
            "k": 0.03519,
            "m": 1.4199
        }
    }
}

average_max = int(values[country][forest]["A"])
st.write(f"The average asymptote maximum biomass yield is {average_max}.")

A = st.number_input("Enter your expected asymptote maximum biomass yield (default if unknown).", value=average_max)

def chapman_richards(t, A, k, m):
    return A * (1 - np.exp(-k * t))**m

year = np.arange(101)
k = values[country][forest]["k"]
m = values[country][forest]["m"]

predicted_series = chapman_richards(year, A, k, m)
cumulative_series = np.cumsum(predicted_series)

plt.figure(figsize=(10, 6))
plt.plot(year, predicted_series, color='red', label='Predicted Annual Carbon Accumulation')
plt.xlabel('Year')
plt.ylabel('CO2e/ha')
plt.title(f'Annual Carbon Accumulation on {forest} ({country})')
plt.legend()
st.pyplot(plt)

selected_year = st.slider("Select a year", 0, 100, 0)
predicted_value = chapman_richards(selected_year, A, k, m)
st.info(f"The predicted carbon accumulation for year {selected_year} is {predicted_value:.2f} CO2e/ha.")

# Display the cumulative carbon accumulation for the selected year
cumulative_value = cumulative_series[selected_year]
st.success(f"The total carbon accumulated up to year {selected_year} is {cumulative_value:.2f} CO2e/ha.")
