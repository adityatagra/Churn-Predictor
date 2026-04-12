import streamlit as st
import pickle
import pandas as pd

# Load model and columns
model = pickle.load(open("model.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

st.title("📊 Customer Churn Prediction")

# Create base input
input_data = pd.DataFrame([[0]*len(columns)], columns=columns)

# ---------------- INPUTS ---------------- #

tenure = st.slider("Tenure", 0, 72, 12)
monthly = st.number_input("Monthly Charges", 0.0, 200.0, 50.0)

contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
tech_support = st.selectbox("Tech Support", ["Yes", "No"])
online_security = st.selectbox("Online Security", ["Yes", "No"])

# ---------------- FILL NUMERIC ---------------- #

if "tenure" in input_data.columns:
    input_data["tenure"] = tenure

if "MonthlyCharges" in input_data.columns:
    input_data["MonthlyCharges"] = monthly

# ---------------- CONTRACT ---------------- #

if contract == "One year":
    if "Contract_One year" in input_data.columns:
        input_data["Contract_One year"] = 1

elif contract == "Two year":
    if "Contract_Two year" in input_data.columns:
        input_data["Contract_Two year"] = 1

# ---------------- INTERNET ---------------- #

if internet == "Fiber optic":
    if "InternetService_Fiber optic" in input_data.columns:
        input_data["InternetService_Fiber optic"] = 1

elif internet == "No":
    if "InternetService_No" in input_data.columns:
        input_data["InternetService_No"] = 1

# ---------------- TECH SUPPORT ---------------- #

if tech_support == "Yes":
    if "TechSupport_Yes" in input_data.columns:
        input_data["TechSupport_Yes"] = 1

# ---------------- ONLINE SECURITY ---------------- #

if online_security == "Yes":
    if "OnlineSecurity_Yes" in input_data.columns:
        input_data["OnlineSecurity_Yes"] = 1

# ---------------- DEFAULT FIX ---------------- #

# Set remaining Yes/No features safely
for col in input_data.columns:
    if "Yes" in col and input_data[col].iloc[0] == 0:
        input_data[col] = 0
    if "No" in col and input_data[col].iloc[0] == 0:
        input_data[col] = 1

# ---------------- PREDICTION ---------------- #

if st.button("Predict"):
    pred = model.predict(input_data)[0]
    prob = model.predict_proba(input_data)[0][1]

    if pred == 1:
        st.error(f"⚠️ High Risk of Churn ({prob:.2f})")
    else:
        st.success(f"✅ Low Risk of Churn ({prob:.2f})")
