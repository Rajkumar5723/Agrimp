from pymongo import MongoClient
from datetime import datetime

def get_database():
    CONNECTION_STRING = "mongodb+srv://username:password@cluster0.9jcddh7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(CONNECTION_STRING)
    return client["soil_fertility_db"]

def log_fertility_result(features, result):
    db = get_database()
    db["fertility_predictions"].insert_one({
        "timestamp": datetime.utcnow(),
        "features": features,
        "result": result
    })

def log_crop_recommendation(inputs, recommended_crops):
    db = get_database()
    db["crop_recommendations"].insert_one({
        "timestamp": datetime.utcnow(),
        "inputs": inputs,
        "recommended_crops": recommended_crops
    })

def log_detailed_fertility_report(features, infertile_details):
    db = get_database()
    db["detailed_reports"].insert_one({
        "timestamp": datetime.utcnow(),
        "features": features,
        "infertile_details": infertile_details
    })