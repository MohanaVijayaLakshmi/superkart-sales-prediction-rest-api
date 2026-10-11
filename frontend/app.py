import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("SuperKart Sales Revenue Prediction")

# Section for online prediction
st.subheader("Online Prediction")

# Collect user input for SuperKart sales prediction

product_weight = st.number_input(
    "Product Weight",
    min_value=0.0,
    step=0.1,
    value=12.66
)

product_allocated_area = st.number_input(
    "Product Allocated Area",
    min_value=0.0,
    max_value=1.0,
    step=0.001,
    value=0.05,
    format="%.3f"
)

product_mrp = st.number_input(
    "Product MRP",
    min_value=0.0,
    step=1.0,
    value=150.0
)

store_age = st.number_input(
    "Store Age",
    min_value=0,
    max_value=100,
    step=1,
    value=15
)

product_sugar_content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "Regular", "No Sugar"]
)

store_size = st.selectbox(
    "Store Size",
    ["Small", "Medium", "High"]
)

store_location_city_type = st.selectbox(
    "Store Location City Type",
    ["Tier 1", "Tier 2", "Tier 3"]
)

store_type = st.selectbox(
    "Store Type",
    [
        "Departmental Store",
        "Supermarket Type1",
        "Supermarket Type2",
        "Food Mart"
    ]
)

product_category = st.selectbox(
    "Product Category",
    ["Food","Non-Consumable","Drinks"]
)

product_perishability = st.selectbox(
    "Product Type",
    ["Non Perishables", "Perishables"]
)

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    'Product_Weight': product_weight,
    'Product_Allocated_Area': product_allocated_area,
    'Product_MRP': product_mrp,
    'Store_Age': store_age,
    'Product_Sugar_Content': product_sugar_content,
    'Store_Size': store_size,
    'Store_Location_City_Type': store_location_city_type,
    'Store_Type': store_type,
    'Product_Category': product_category,
    'Product_Perishability': product_perishability
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/predictsales", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Predicted Sales (in dollars)']
        st.success(f"Predicted total sales (in dollars): {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")
