import numpy as np
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize the Flask application
superkart_sales_predictor_api = Flask("Super Kart Sales Predictor")

# Load the trained machine learning model
model = joblib.load("../models/superkart_sales_prediction_model_v1_0.joblib")

@superkart_sales_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the Super Kart Sales Prediction API!"

@superkart_sales_predictor_api.post('/v1/predictsales')
def predict_sales():
    """
    This function handles POST requests to the '/v1/predictsales' endpoint.
    It expects a JSON payload containing product and store details and returns
    the predicted sales as a JSON response.
    """
    try:
        # Get the JSON data from the request body
        input_data_json = request.get_json()

        # Extract relevant features from the JSON data
        sample = {
            'Product_Weight': input_data_json['Product_Weight'],
            'Product_Sugar_Content': input_data_json['Product_Sugar_Content'],
            'Product_Allocated_Area': input_data_json['Product_Allocated_Area'],
            'Product_Type': input_data_json['Product_Type'],
            'Product_MRP': input_data_json['Product_MRP'],
            'Store_Id': input_data_json['Store_Id'],
            'Store_Size': input_data_json['Store_Size'],
            'Store_Location_City_Type': input_data_json['Store_Location_City_Type'],
            'Store_Type': input_data_json['Store_Type'],
            'Store_Age': input_data_json['Store_Age']
        }

        # Convert the extracted data into a Pandas DataFrame
        input_df = pd.DataFrame([sample])

        # Make prediction
        predicted_sales = model.predict(input_df)[0]

        # Convert predicted_sales to Python float and round
        predicted_sales = round(float(predicted_sales), 2)

        # Return the predicted sales
        return jsonify({'Predicted_Product_Store_Sales_Total': predicted_sales})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@superkart_sales_predictor_api.post('/v1/batchpredictsales')
def predict_sales_batch():
    """
    This function handles POST requests to the '/v1/batchpredictsales' endpoint.
    It expects a CSV file containing product and store details for multiple entries
    and returns the predicted sales as a JSON response.
    """
    try:
        # Get the uploaded CSV file from the request
        file = request.files['file']

        # Read the CSV file into a Pandas DataFrame
        input_df_batch = pd.read_csv(file)

        # Make predictions for all entries in the DataFrame
        predicted_sales_batch = model.predict(input_df_batch).tolist()

        # Convert predicted_sales to Python floats and round
        predicted_sales_batch = [round(float(sales), 2) for sales in predicted_sales_batch]

        # Return the predictions list as a JSON response
        return jsonify({'Predicted_Product_Store_Sales_Totals': predicted_sales_batch})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    superkart_sales_predictor_api.run(debug=True)