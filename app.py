

import streamlit as st
import pickle
import numpy as np

model = pickle.load(open("model.pkl", "rb"))

st.title("Customer Churn Prediction")

tenure = st.slider("Tenure", 0, 72)
monthly = st.number_input("Monthly Charges")

if st.button("Predict"):
    input_data = np.array([[tenure, monthly]])
    prediction = model.predict(input_data)

    if prediction[0] == 1:
        st.error("Customer will churn")
    else:
        st.success("Customer will stay")
