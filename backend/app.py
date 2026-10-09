# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
sales_predictor_api = Flask("Superkart Sales Revenue Predictor")

# Load the trained machine learning model
model = joblib.load("superkart_model.joblib")

# Define a route for the home page (GET request)
@sales_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the Superkart Sales Revenue Prediction API!"

# Define an endpoint for single property prediction (POST request)
@sales_predictor_api.post('/v1/predictsales')
def predict_sales():
    """
    This function handles POST requests to the '/v1/predictsales' endpoint.
    It expects a JSON payload containing property details and returns
    the predicted rental price as a JSON response.
    """
    # Get the JSON data from the request body
    property_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Weight': property_data['Product_Weight'],
        'Product_Allocated_Area': property_data['Product_Allocated_Area'],
        'Product_MRP': property_data['Product_MRP'],
        'Store_Age': property_data['Store_Age'],
        'Product_Sugar_Content': property_data['Product_Sugar_Content'],
        'Store_Size': property_data['Store_Size'],
        'Store_Location_City_Type': property_data['Store_Location_City_Type'],
        'Store_Type': property_data['Store_Type'],
        'Product_Category': property_data['Product_Category'],
        'Product_Perishability': property_data['Product_Perishability']

    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction (get log_price)
    predicted_sales = model.predict(input_data)[0]

    # Return the actual sales
    return jsonify({'Predicted Total Sales (in dollars)': round(float(predicted_sales), 2)
})


# Define an endpoint for batch prediction (POST request)
@sales_predictor_api.post('/v1/predictbatch')
def predict_rental_price_batch():
    """
    This function handles POST requests to the '/v1/predictbatch' endpoint.
    It expects a CSV file containing property details for multiple properties
    and returns the predicted rental prices as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all properties in the DataFrame (get log_prices)
    predicted_sales = model.predict(input_data).tolist()

    # Return the predictions dictionary as a JSON response
    return predicted_sales

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    sales_predictor_api.run(debug=True)
