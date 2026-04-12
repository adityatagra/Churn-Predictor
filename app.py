import streamlit as st
import pickle
import pandas as pd

# Load model and columns
model = pickle.load(open("model.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

st.set_page_config(page_title="Churn Prediction", layout="centered")

st.title("📊 Customer Churn Prediction")
st.write("Fill customer details to predict churn probability")

# Create empty dataframe
input_data = pd.DataFrame([[0]*len(columns)], columns=columns)

# ---------------- INPUTS ---------------- #

tenure = st.slider("Tenure (months)", 0, 72, 12)
monthly_charges = st.number_input("Monthly Charges", 0.0, 200.0, 50.0)

contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

# ---------------- FILL DATA ---------------- #

# Numeric
if "tenure" in input_data.columns:
    input_data["tenure"] = tenure

if "MonthlyCharges" in input_data.columns:
    input_data["MonthlyCharges"] = monthly_charges

# Contract Encoding
if contract == "One year" and "Contract_One year" in input_data.columns:
    input_data["Contract_One year"] = 1
elif contract == "Two year" and "Contract_Two year" in input_data.columns:
    input_data["Contract_Two year"] = 1

# Internet Encoding
if internet == "Fiber optic" and "InternetService_Fiber optic" in input_data.columns:
    input_data["InternetService_Fiber optic"] = 1
elif internet == "No" and "InternetService_No" in input_data.columns:
    input_data["InternetService_No"] = 1

# ---------------- PREDICTION ---------------- #

if st.button("Predict Churn"):
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    st.subheader("🔍 Prediction Result")

    if prediction == 1:
        st.error(f"⚠️ High Risk of Churn\nProbability: {probability:.2f}")
    else:
        st.success(f"✅ Low Risk of Churn\nProbability: {probability:.2f}")

    # Progress bar
    st.progress(float(probability))

    # ---------------- INSIGHTS ---------------- #

    st.subheader("💡 Insights")

    if tenure < 12:
        st.write("- Short tenure customers are more likely to churn")

    if monthly_charges > 70:
        st.write("- High monthly charges increase churn risk")

    if contract == "Month-to-month":
        st.write("- Month-to-month contracts have higher churn")

