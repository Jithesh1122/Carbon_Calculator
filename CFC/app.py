import streamlit as st
import pandas as pd
import plotly.express as px
from modules.chatbot import CarbonFootprintChatbot
from modules.location_services import LocationServices

# Streamlit settings
st.set_page_config(layout="wide", page_title="Carbon Calculator")

# Initialize services
chatbot = CarbonFootprintChatbot()
location_services = LocationServices()

# Load emission factors
EMISSION_FACTORS = {
    "Car": 0.2, "Bus": 0.1, "Train": 0.05, "Motorcycle": 0.1, "Airplane": 0.25,
    "Electricity": 0.85, "LPG": 2.5, "CNG": 2.2,
    "Vegan": 0.5, "Vegetarian": 0.8, "Non-vegetarian": 1.5,
    "Organic": 0.5, "Plastic": 2.5, "Paper": 1.0, "Metal": 2.0
}

# App sections
st.title("🌍 Carbon Footprint Calculator")
tab1, tab2, tab3 = st.tabs(["📊 Calculate", "🌍 Air Quality", "💬 Chat"])

with tab1:
    st.header("Calculate Your Carbon Footprint")

    transport_type = st.selectbox("🚗 Transport Mode", ["Car", "Bus", "Train", "Motorcycle", "Airplane"])
    distance = st.slider("Daily commute distance (km)", 0.0, 100.0, 10.0)

    diet_type = st.selectbox("🍽️ Diet Type", ["Vegan", "Vegetarian", "Non-vegetarian"])
    meals = st.number_input("Meals per day", 1, 6, 3)

    electricity = st.slider("💡 Monthly Electricity Usage (kWh)", 0.0, 1000.0, 200.0)
    waste_plastic = st.slider("🗑️ Plastic Waste (kg/week)", 0.0, 10.0, 1.0)

    if st.button("Calculate"):
        transport_emissions = EMISSION_FACTORS[transport_type] * distance * 365 / 1000
        diet_emissions = EMISSION_FACTORS[diet_type] * meals * 365 / 1000
        energy_emissions = EMISSION_FACTORS["Electricity"] * electricity * 12 / 1000
        waste_emissions = EMISSION_FACTORS["Plastic"] * waste_plastic * 52 / 1000

        total_emissions = round(transport_emissions + diet_emissions + energy_emissions + waste_emissions, 2)
        st.success(f"🌍 Your total annual carbon footprint is {total_emissions} tonnes CO2")

        df = pd.DataFrame({"Category": ["Transport", "Diet", "Energy", "Waste"],
                           "Emissions (tonnes CO2)": [transport_emissions, diet_emissions, energy_emissions, waste_emissions]})
        fig = px.pie(df, values='Emissions (tonnes CO2)', names='Category', title="Emission Breakdown")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("🌍 Air Quality Check")
    latitude = st.number_input("Enter latitude", -90.0, 90.0, 20.5937)
    longitude = st.number_input("Enter longitude", -180.0, 180.0, 78.9629)

    if st.button("Check Air Quality"):
        air_quality = location_services.get_air_quality(latitude, longitude)
        if air_quality:
            st.info(f"AQI: {air_quality['aqi']} - {air_quality['status']}")

with tab3:
    st.header("💬 Chat with Eco Assistant")
    user_message = st.text_input("Ask a question:")
    if st.button("Send"):
        response = chatbot.get_response(user_message)
        st.write(response)
