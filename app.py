import streamlit as st
import matplotlib.pyplot as plt

st.image("logo.webp")

st.title("🌍 Simple Carbon Footprint Calculator")

st.write("Answer the following questions to calculate your carbon footprint score.")

# Create two columns
col1, col2 = st.columns(2)

with col1:
    st.header("🚗 Transportation")

    # Question 1: Car usage
    car_miles = st.number_input("Average miles driven per week:", min_value=0, max_value=5000, value=100)
    car_type = st.selectbox("Type of car:", ["Gasoline", "Diesel", "Hybrid", "Electric", "None"])

    # Question 2: Flights
    flights_per_year = st.number_input("Number of flights per year:", min_value=0, max_value=50, value=1)

    
with col2:
    st.header("⚡Energy Use")

    Laundry = st.number_input("How often do you do your laundry per month?", min_value=0, max_value=15, value=2)
    lights_off = st.selectbox("Do you turn the light off when you leave a room:", ["Yes", "No"])
    A_C = st.selectbox("What is your AC like?", ["60-65", "66-70", "71-75", "76-80", "Off"])

    
# Create two columns for diet section
co1, co2, co3 = st.columns(3)

with co2:
    st.header("🥗 Diet")

    # Question 4: Diet type
    diet_type = st.selectbox("Your diet type:", ["Meat-heavy", "Omnivore", "Vegetarian", "Vegan"])

    calculate = st.button("Calculate Carbon Footprint")

if calculate:
    # Initialize total emissions
    total_emissions = 0
    emission_details = {}

    # Transportation Emissions
    transport_emissions = 0

    # Car Emissions
    if car_type != "None":
        car_emission_factors = {
            "Gasoline": 0.411,  # kg CO₂ per mile
            "Diesel": 0.371,
            "Hybrid": 0.200,
            "Electric": 0.0  # Assuming zero emissions for electric car (can be adjusted)
        }
        annual_car_emissions = car_miles * 52 * car_emission_factors.get(car_type, 0.411)
        transport_emissions += annual_car_emissions
        emission_details['Car'] = annual_car_emissions

    # Flights Emissions
    flight_emission_factor = 250  # kg CO₂ per flight (average)
    annual_flight_emissions = flights_per_year * flight_emission_factor
    transport_emissions += annual_flight_emissions
    emission_details['Flights'] = annual_flight_emissions

    total_emissions += transport_emissions

    # Energy Use Emissions
    energy_emissions = 0
    # Electricity Emission Factor (average 0.233 kg CO₂ per kWh)
    electricity_emission_factor = 0.233
    annual_electricity_emissions = 12 * electricity_emission_factor
    energy_emissions += annual_electricity_emissions

    # Emission from other factors (laundry, lights, AC)
    # Add arbitrary values for these based on assumed behavior (adjust as needed)
    laundry_emission_factor = 1.5  # kg CO₂ per laundry cycle
    laundry_emissions = Laundry * 12 * laundry_emission_factor
    energy_emissions += laundry_emissions

    lights_off_emissions = 0 if lights_off == "Yes" else 100  # Arbitrary value if lights are left on
    energy_emissions += lights_off_emissions

    # AC emissions based on temperature preference (adjust values as needed)
    ac_emission_factors = {
        "60-65": 500,  # High AC usage
        "66-70": 300,
        "71-75": 150,
        "76-80": 50,
        "Off": 0
    }
    ac_emissions = ac_emission_factors.get(A_C, 150)
    energy_emissions += ac_emissions

    # Add energy emissions to total and details
    total_emissions += energy_emissions
    emission_details['Energy Use'] = energy_emissions

    # Diet Emissions
    diet_emission_factors = {
        "Meat-heavy": 3.0,  # tons CO₂ per year
        "Omnivore": 2.5,
        "Vegetarian": 1.7,
        "Vegan": 1.5
    }

    diet_emissions = diet_emission_factors.get(diet_type, 2.5) * 1000  # Convert tons to kg
    emission_details['Diet'] = diet_emissions
    total_emissions += diet_emissions

    # Final Output
    st.header("Your Carbon Footprint Results")

    st.write(f"**Total Annual Carbon Footprint:** {total_emissions:.2f} kg CO₂e")

    # Convert to a score from 1 to 500
    # Assuming average emissions are 10,000 kg CO₂e per year
    score = (total_emissions / 10000) * 500  # Maximum score is 500
    score = min(max(score, 1), 500)
    st.subheader(f"Your Carbon Footprint Score: **{int(score)}** (1=Best, 500=Worst)")

    # Breakdown Chart
    labels = list(emission_details.keys())
    emissions = [emission_details[label] for label in labels]

    # Pie Chart for Carbon Footprint Breakdown
    c1 , c2 = st.columns(2)
    with c1:
        fig1, ax1 = plt.subplots()
        ax1.pie(emissions, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)

    # Bar Chart for Carbon Footprint Breakdown
    with c2:
        fig2, ax2 = plt.subplots()
        ax2.bar(labels, emissions, color='green')
        ax2.set_ylabel('Emissions (kg CO₂e)')
        ax2.set_title('Carbon Footprint Breakdown')
        st.pyplot(fig2)