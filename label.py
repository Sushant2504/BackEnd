from sklearn.preprocessing import LabelEncoder
import joblib

# Example encoding for soil type
soil_encoder = LabelEncoder()
soil_encoder.fit(["Sandy", "Loamy", "Clayey", "Black", "Red"])  # fit on all possible categories
joblib.dump(soil_encoder, 'soil_label_encoder.joblib')

# Similarly, for crop type:
crop_types = [
    "Barley", "Cotton", "Ground Nuts", "Maize", "Millets", "Oil seeds", "Paddy", 
    "Pulses", "Sugarcane", "Tobacco", "Wheat", "coffee", "kidneybeans", "orange", 
    "pomegranate", "rice", "watermelon"
]

# Initialize LabelEncoder
crop_encoder = LabelEncoder()

# Fit the encoder with crop types
crop_encoder.fit(crop_types)

# Save the encoder using joblib
joblib.dump(crop_encoder, 'crop_label_encoder.joblib')