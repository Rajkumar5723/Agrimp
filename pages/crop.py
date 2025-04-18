import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# MongoDB Setup
def get_database():
    CONNECTION_STRING = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    return client["soil_fertility_db"]

def log_crop_recommendation(inputs, recommended):
    db = get_database()
    db["crop_recommendations"].insert_one({
        "timestamp": datetime.utcnow(),
        "inputs": inputs,
        "recommended_crops": recommended
    })

# Crop Ranges (after rice cultivation)
crop_nutrient_ranges = {
    "Wheat":  {"N": (200, 280), "P": (10, 25), "K": (110, 280), "Ca": (1000, 2000), "Mg": (100, 300), "S": (15, 30), "Zn": (0.6, 1.5), "B": (0.5, 1.5), "pH": (6.5, 7.5), "OC": (0.5, 0.8)},
    "Maize":  {"N": (220, 280), "P": (12, 22), "K": (150, 270), "Ca": (1000, 1800), "Mg": (100, 250), "S": (18, 28), "Zn": (0.8, 1.5), "B": (0.6, 1.4), "pH": (6.2, 7.5), "OC": (0.5, 0.8)},
    "Barley": {"N": (240, 280), "P": (15, 25), "K": (110, 200), "Ca": (1000, 1600), "Mg": (100, 220), "S": (15, 25), "Zn": (0.7, 1.3), "B": (0.5, 1.2), "pH": (6.5, 7.5), "OC": (0.5, 0.75)},
    "Soybean":{"N": (200, 250), "P": (10, 25), "K": (140, 250), "Ca": (1200, 2000), "Mg": (150, 300), "S": (15, 30), "Zn": (0.6, 1.2), "B": (0.5, 1.5), "pH": (5.8, 7.2), "OC": (0.5, 0.8)}
}

# Streamlit Page
st.set_page_config(page_title="Crop Recommendation", layout="centered")
st.title("🌾 Crop Recommendation After Rice Cultivation")

# Input fields
inputs = {
    "N": st.number_input("Nitrogen (N) [kg/ha]", 100, 300, 220),
    "P": st.number_input("Phosphorus (P) [kg/ha]", 5, 50, 15),
    "K": st.number_input("Potassium (K) [kg/ha]", 100, 300, 150),
    "Ca": st.number_input("Calcium (Ca) [mg/kg]", 900, 2100, 1200),
    "Mg": st.number_input("Magnesium (Mg) [mg/kg]", 80, 350, 150),
    "S": st.number_input("Sulfur (S) [mg/kg]", 10, 40, 20),
    "Zn": st.number_input("Zinc (Zn) [mg/kg]", 0.5, 2.0, 1.0),
    "B": st.number_input("Boron (B) [mg/kg]", 0.4, 2.0, 0.8),
    "pH": st.number_input("Soil pH", 5.0, 8.5, 6.5),
    "OC": st.number_input("Organic Carbon (%)", 0.4, 1.0, 0.6)
}

def get_suitable_crops(data):
    result = []
    for crop, limits in crop_nutrient_ranges.items():
        if all(limits[k][0] <= data[k] <= limits[k][1] for k in limits):
            result.append(crop)
    return result

# Recommend crops
if st.button("🌾 Recommend Crops"):
    recommended = get_suitable_crops(inputs)
    
    if recommended:
        st.success(f"✅ Suitable Crops: {', '.join(recommended)}")
    else:
        st.warning("⚠️ No suitable crops match these conditions.")

    try:
        log_crop_recommendation(inputs, recommended)
        st.info("📝 Recommendation stored in MongoDB.")
    except Exception as e:
        st.error(f"❌ MongoDB Error: {e}")