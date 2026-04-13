import streamlit as st
import pickle
import pandas as pd

# Load model and columns
model = pickle.load(open("model.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

st.title("Customer Churn Prediction App")

st.write("Enter customer details to predict churn")

# Create empty dataframe with all features
input_data = pd.DataFrame([[0]*len(columns)], columns=columns)

# --- USER INPUTS ---
tenure = st.slider("Tenure (months)", 0, 72, 12)
monthly_charges = st.number_input("Monthly Charges", 0.0, 200.0, 50.0)

contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

# --- FILL DATA ---
if "tenure" in input_data.columns:
    input_data["tenure"] = tenure

if "MonthlyCharges" in input_data.columns:
    input_data["MonthlyCharges"] = monthly_charges

# Handle contract encoding
if contract == "One year" and "Contract_One year" in input_data.columns:
    input_data["Contract_One year"] = 1
elif contract == "Two year" and "Contract_Two year" in input_data.columns:
    input_data["Contract_Two year"] = 1

# Handle internet encoding
if internet == "Fiber optic" and "InternetService_Fiber optic" in input_data.columns:
    input_data["InternetService_Fiber optic"] = 1
elif internet == "No" and "InternetService_No" in input_data.columns:
    input_data["InternetService_No"] = 1

# --- PREDICTION ---
if st.button("Predict"):
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    if prediction == 1:
        st.error(f"⚠️ Customer is likely to churn\nProbability: {probability:.2f}")
    else:
        st.success(f"✅ Customer is likely to stay\nProbability: {probability:.2f}")
