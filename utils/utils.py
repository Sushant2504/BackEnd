import numpy as np
from joblib import load

# Load models and encoders
def get_crop_recommendation(data, model):
    crop_data = np.array([
        [data.nitrogen, data.phosphorus, data.potassium, data.temperature, data.humidity, data.ph, data.rainfall]
    ])
    crop_prediction = model.predict(crop_data)
    return crop_prediction[0]

def get_fertilizer_recommendation(data, model, soil_encoder, crop_encoder, fertilizer_encoder):
    soil_type_encoded = soil_encoder.transform([data.soil_type])[0]
    crop_type_encoded = crop_encoder.transform([data.crop_type])[0]
    
    fertilizer_data = np.array([[ 
        data.temperature, 
        data.humidity, 
        data.moisture, 
        soil_type_encoded, 
        crop_type_encoded, 
        data.nitrogen, 
        data.potassium, 
        data.phosphorous
    ]])

    fertilizer_prediction_encoded = model.predict(fertilizer_data)
    fertilizer_prediction = fertilizer_encoder.inverse_transform(fertilizer_prediction_encoded)
    return fertilizer_prediction[0]
