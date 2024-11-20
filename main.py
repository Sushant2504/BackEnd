import streamlit as st
import pickle
import numpy as np
from joblib import load
from sklearn.preprocessing import StandardScaler
import joblib

# Load the models and scalers for both tasks
with open('Models/RandomForest.pkl', 'rb') as crop_model_file:
    crop_model = pickle.load(crop_model_file)
    
soil_label_encoder = load('Models/soil_label_encoder.joblib')  # For encoding Soil Type
crop_label_encoder = load('Models/crop_label_encoder.joblib')  # For encoding Crop Type

with open('Models/fertilizer.pkl', 'rb') as fertilizer_model_file:
    fertilizer_model = pickle.load(fertilizer_model_file)

fertilizer_label_encoder = load('Models/fertilizer_encoder.joblib')

# Chatbot Title
st.title("Farming Assistant Chatbot")

# Step 1: Ask user to choose between options
option = st.radio(
    "What would you like assistance with?",
    ("Crop Recommendation", "Fertilizer Recommendation")
)

# Step 2: Dynamic questions based on the selected option
if option == "Crop Recommendation":
    st.subheader("Answer the following questions for Crop Recommendation:")
    N = st.text_input("Enter Nitrogen (N):", placeholder="e.g., 50")
    P = st.text_input("Enter Phosphorus (P):", placeholder="e.g., 30")
    K = st.text_input("Enter Potassium (K):", placeholder="e.g., 20")
    temperature = st.text_input("Enter Temperature (°C):", placeholder="e.g., 25.5")
    humidity = st.text_input("Enter Humidity (%):", placeholder="e.g., 80")
    pH = st.text_input("Enter pH:", placeholder="e.g., 6.5")
    rainfall = st.text_input("Enter Rainfall (mm):", placeholder="e.g., 200")

    if st.button("Submit for Crop Recommendation"):
        if all([N, P, K, temperature, humidity, pH, rainfall]):
            try:
                # Process inputs and make predictions
                crop_data = np.array([
                    [float(N), float(P), float(K), float(temperature), float(humidity), float(pH), float(rainfall)]
                ])        
                crop_prediction = crop_model.predict(crop_data)
                st.success(f"Recommended Crop: {crop_prediction[0]}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please fill all fields for Crop Recommendation.")

elif option == "Fertilizer Recommendation":
    st.subheader("Answer the following questions for Fertilizer Recommendation:")
    
    # Input fields
    temperature = st.text_input("Enter Temperature (°C):", placeholder="e.g., 30")
    humidity = st.text_input("Enter Humidity (%):", placeholder="e.g., 75")
    moisture = st.text_input("Enter Moisture (%):", placeholder="e.g., 12.5")
    soil_type = st.selectbox("Select Soil Type:", ["Sandy", "Loamy", "Clayey", "Black", "Red"])
    crop_type = st.selectbox("Select Crop Type:", [
        "Barley", "Cotton", "Ground Nuts", "Maize", "Millets", "Oil seeds", "Paddy", 
        "Pulses", "Sugarcane", "Tobacco", "Wheat", "coffee", "kidneybeans", "orange", 
        "pomegranate", "rice", "watermelon"
    ])
    nitrogen = st.text_input("Enter Current Nitrogen (N) Level:", placeholder="e.g., 20")
    potassium = st.text_input("Enter Current Potassium (K) Level:", placeholder="e.g., 10")
    phosphorous = st.text_input("Enter Current Phosphorous (P) Level:", placeholder="e.g., 15")
    
    if st.button("Submit for Fertilizer Recommendation"):
        # Check if all fields are filled
        if all([temperature, humidity, moisture, soil_type, crop_type, nitrogen, potassium, phosphorous]):
            try:
                # Encode categorical inputs using LabelEncoder
                soil_type_encoded = soil_label_encoder.transform([soil_type])[0]
                crop_type_encoded = crop_label_encoder.transform([crop_type])[0]
            
                # Prepare input data
                fertilizer_data = np.array([[
                    float(temperature),
                    float(humidity),
                    float(moisture),
                    soil_type_encoded,
                    crop_type_encoded,
                    float(nitrogen),
                    float(potassium),
                    float(phosphorous),
                ]])

                # Predict the fertilizer recommendation (encoded)
                fertilizer_prediction_encoded = fertilizer_model.predict(fertilizer_data)
                
                # Decode the prediction to get the original fertilizer name
                fertilizer_prediction = fertilizer_label_encoder.inverse_transform(fertilizer_prediction_encoded)
                st.success(f"Recommended Fertilizer: {fertilizer_prediction[0]}")
                

            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please fill all fields for Fertilizer Recommendation.")


# Step 3: General Conversation Questions
st.divider()
st.subheader("Chatbot Mode")
user_message = st.text_input("You can ask me general questions here:")
if user_message:
    st.write(f"Chatbot: I'm still learning, but I appreciate your question: '{user_message}'")