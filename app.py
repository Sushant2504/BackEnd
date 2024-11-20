from fastapi import FastAPI, HTTPException
import joblib
from pydantic import BaseModel
from typing import List
import numpy as np
import pickle
from joblib import load
from utils.utils import get_crop_recommendation, get_fertilizer_recommendation

app = FastAPI()

# Load models and encoders
crop_model = pickle.load(open('Models/RandomForest.pkl', 'rb'))
fertilizer_model = pickle.load(open('Models/fertilizer.pkl', 'rb'))
soil_label_encoder = joblib.load('Models/soil_label_encoder.joblib')
crop_label_encoder = joblib.load('Models/crop_label_encoder.joblib')
fertilizer_label_encoder = joblib.load('Models/fertilizer_encoder.joblib')

class CropInput(BaseModel):
    nitrogen: float
    phosphorus: float
    potassium: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float

class FertilizerInput(BaseModel):
    temperature: float
    humidity: float
    moisture: float
    soil_type: str
    crop_type: str
    nitrogen: float
    potassium: float
    phosphorous: float

class PredictionResponse(BaseModel):
    recommended_crop: str = None
    recommended_fertilizer: str = None

@app.post("/crop_recommendation/", response_model=PredictionResponse)
async def crop_recommendation(data: CropInput):
    try:
        recommended_crop = get_crop_recommendation(data, crop_model)
        return {"recommended_crop": recommended_crop}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/fertilizer_recommendation/", response_model=PredictionResponse)
async def fertilizer_recommendation(data: FertilizerInput):
    try:
        recommended_fertilizer = get_fertilizer_recommendation(data, fertilizer_model, soil_label_encoder, crop_label_encoder, fertilizer_label_encoder)
        return {"recommended_fertilizer": recommended_fertilizer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

