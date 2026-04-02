import streamlit as st
import pickle
import pandas as pd

# Load model and columns
model = pickle.load(open("model.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

st.title("Customer Churn Prediction")

# Create empty input
input_data = pd.DataFrame([[0]*len(columns)], columns=columns)

# Example inputs (expand later)
tenure = st.slider("Tenure", 0, 72)
monthly = st.number_input("Monthly Charges")

# Fill values
if "tenure" in input_data.columns:
    input_data["tenure"] = tenure

if "MonthlyCharges" in input_data.columns:
    input_data["MonthlyCharges"] = monthly

# Predict
if st.button("Predict"):
    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.error("Customer will churn")
    else:
        st.success("Customer will stay")
