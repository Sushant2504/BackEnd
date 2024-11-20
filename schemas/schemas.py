from pydantic import BaseModel
from typing import Optional

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
    recommended_crop: Optional[str] = None
    recommended_fertilizer: Optional[str] = None
