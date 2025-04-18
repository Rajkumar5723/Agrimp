import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# MongoDB Setup
def get_database():
    CONNECTION_STRING = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    return client["soil_fertility_db"]

def log_detailed_fertility_report(features, infertile_details):
    db = get_database()
    db["detailed_reports"].insert_one({
        "timestamp": datetime.utcnow(),
        "features": features,
        "infertile_details": infertile_details
    })

# Streamlit App
st.set_page_config(page_title="Soil Report", layout="centered")
st.title("📊 Detailed Soil Fertility Report")

features = st.session_state.get("features")
infertile_details = st.session_state.get("infertile_details")
fertility_status = st.session_state.get("fertility_status")

if not features:
    st.warning("⚠️ No prediction data found. Go back to the main page and submit values.")
    st.stop()

st.subheader("🌿 Soil Input Summary:")
for key, val in features.items():
    st.write(f"- {key}: {val}")

if fertility_status == "Infertile":
    st.subheader("⚠️ Nutrient Issues Detected:")
    for param, details in infertile_details.items():
        st.markdown(
            f"**{param}** → {details['value']} ({details['issue']}) | Optimal: {details['min']} - {details['max']}"
        )
    try:
        log_detailed_fertility_report(features, infertile_details)
        st.success("📦 Report saved to MongoDB successfully.")
    except Exception as e:
        st.error(f"❌ Failed to store report: {e}")
else:
    st.success("✅ All nutrients are within optimal range.")