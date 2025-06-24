import streamlit as st
import requests
import pandas as pd
st.set_page_config(page_title="PlantPal", page_icon="🌿")
st.title("🌿 PlantPal")
st.subheader("Grow your climate impact. One native plant at a time.")
# Load location data
locations_df = pd.read_csv("locations.csv")

location = st.selectbox(
    "Select your location",
    options=locations_df["Suburb"] + " (" + locations_df["Postcode"].astype(str) + ")",
    index=0,
    help="Start typing to search"
)


spot_type = st.selectbox("🪴 Choose your planting spot", ["Ground", "Pot", "Balcony", "Planter Box"])
sunlight = st.selectbox("☀️ Sunlight exposure", ["Full Sun", "Partial Shade", "Full Shade"])

if location and spot_type and sunlight:
    params = {
        "location": location,
        "spot": spot_type,
        "sunlight": sunlight
    }
    try:
        response = requests.get("http://localhost:8000/recommend", params=params)
        if response.status_code == 200:
            plants = response.json()
            if plants:
                st.write(f"🌱 Recommended Plants for {location} ({spot_type}, {sunlight})")
                for plant in plants:
                    st.markdown(f"""
                    ### 🌿 {plant['Plant']}
                    **Scientific Name:** *{plant.get('Scientific Name', 'N/A')}*  
                    **CO₂ Absorption:** {plant.get('CO₂ Absorption (kg/year)', 'N/A')} kg/year  
                    **Notes:** {plant.get('Notes', 'No notes')}  
                    👉 [Buy Here]({plant.get('Buy Link', '#')})
                    """)
            else:
                st.warning("No matching plants found for your criteria.")
        else:
            st.error("Error fetching data from API.")
    except requests.exceptions.RequestException:
        st.error("Failed to connect to the API. Is your FastAPI server running?")
