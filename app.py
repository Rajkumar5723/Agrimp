import streamlit as st
from datetime import datetime
from pymongo import MongoClient

# MongoDB Setup
def get_database():
    CONNECTION_STRING = "mongodb+srv://abithas2711:Abitha2003@cluster0.9jcddh7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(CONNECTION_STRING)
    return client["soil_fertility_db"]

def log_fertility_result(features, result):
    db = get_database()
    db["fertility_predictions"].insert_one({
        "timestamp": datetime.utcnow(),
        "features": features,
        "fertility_prediction": result
    })

# Optimal Ranges
optimal_ranges = {
    'pH': (6.0, 6.5),
    'EC': (0.8, 1.8),
    'OC': (0.28, 6.00),
    'N': (0.03, 0.07),
    'P': (0.10, 0.225),
    'K': (1.28, 2.77),
    'Zn': (0.001, 0.005),
    'Fe': (0.01, 0.05),
    'Cu': (5, 20),
    'Mn': (0.002, 0.005),
    'Cl': (0.1, 0.5),
    'CaCO3': (20, 48),
    'OM': (3, 5),
    'Sand': (40, 60),
    'Silt': (20, 40),
    'Clay': (20, 40),
    'CEC': (10, 20),
    'Boron': (0.5, 1.0),
    'Magnesium': (50, 150),
    'S': (0.1, 0.4)
}

maintenance_recommendations = [
    "Practice crop rotation to prevent nutrient depletion.",
    "Use green manure and organic compost to enhance soil fertility.",
    "Ensure proper irrigation to prevent erosion and nutrient leaching.",
    "Regularly test soil nutrients and adjust fertilization accordingly.",
    "Encourage microbial activity with organic matter and biofertilizers."
]

# Streamlit App
st.set_page_config(page_title="Soil Fertility Predictor", layout="centered")
st.title("🌱 Soil Fertility Prediction")

features = {}
for nutrient, (min_val, max_val) in optimal_ranges.items():
    features[nutrient] = st.number_input(
        f"{nutrient}", 
        min_value=float(min_val) * 0.5,
        max_value=float(max_val) * 1.5,
        value=(min_val + max_val) / 2
    )

if st.button("Predict Soil Fertility"):
    deficient_nutrients = [param for param, value in features.items()
                           if value < optimal_ranges[param][0] or value > optimal_ranges[param][1]]
    
    fertility_status = "Infertile" if deficient_nutrients else "Fertile"
    st.success(f"The soil is predicted to be: **{fertility_status}**")

    try:
        log_fertility_result(features, fertility_status)
        st.info("📝 Stored prediction in MongoDB successfully.")
    except Exception as e:
        st.error(f"❌ MongoDB Error: {e}")

    # Save data to session state
    st.session_state.features = features
    st.session_state.fertility_status = fertility_status

    if fertility_status == "Infertile":
        st.session_state.infertile_details = {
            param: {
                "value": features[param],
                "min": optimal_ranges[param][0],
                "max": optimal_ranges[param][1],
                "issue": "Too Low" if features[param] < optimal_ranges[param][0] else "Too High"
            }
            for param in deficient_nutrients
        }
    else:
        st.session_state.infertile_details = {}

    # Report Content
    report_content = "📄 Soil Fertility Analysis Report\n\n"
    report_content += f"Soil Status: {fertility_status}\n\n"

    if fertility_status == "Infertile":
        report_content += "**Nutrient Deficiencies & Recommendations:**\n"
        for param in deficient_nutrients:
            value = features[param]
            min_val, max_val = optimal_ranges[param]
            issue = "🔴 Too Low" if value < min_val else "🔴 Too High"
            report_content += f"- {param}: {value} ({issue}). Adjust accordingly.\n"
    else:
        report_content += "**Best Practices for Alluvial Soil Maintenance:**\n"
        for tip in maintenance_recommendations:
            report_content += f"- {tip}\n"

    # Download Report
    st.download_button(
        label="📥 Download Soil Report",
        data=report_content,
        file_name="soil_fertility_report.txt",
        mime="text/plain"
    )

    if st.button("📊 View Detailed Report"):
        st.switch_page("pages/report.py")
