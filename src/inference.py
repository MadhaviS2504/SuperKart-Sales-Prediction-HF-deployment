import pandas as pd
import joblib
import numpy as np

def load_model(model_path):
    """Load the trained model from disk."""
    return joblib.load(model_path)

def predict_single(model, input_data):
    """Make prediction for a single data point."""
    # Convert input to DataFrame
    input_df = pd.DataFrame([input_data])

    # Make prediction
    prediction = model.predict(input_df)[0]

    return round(float(prediction), 2)

def predict_batch(model, input_df):
    """Make predictions for a batch of data points."""
    predictions = model.predict(input_df).tolist()
    return [round(float(pred), 2) for pred in predictions]

if __name__ == "__main__":
    # Load model
    model = load_model('../models/superkart_sales_prediction_model_v1_0.joblib')

    # Example single prediction
    sample_input = {
        'Product_Weight': 12.0,
        'Product_Sugar_Content': 'Regular',
        'Product_Allocated_Area': 0.05,
        'Product_Type': 'Snack Foods',
        'Product_MRP': 150.0,
        'Store_Id': 'OUT004',
        'Store_Size': 'Medium',
        'Store_Location_City_Type': 'Tier 2',
        'Store_Type': 'Supermarket Type2',
        'Store_Age': 17
    }

    prediction = predict_single(model, sample_input)
    print(f"Predicted sales: ${prediction}")

    # Example batch prediction
    batch_data = pd.DataFrame([sample_input, sample_input])  # Duplicate for example
    batch_predictions = predict_batch(model, batch_data)
    print(f"Batch predictions: {batch_predictions}")