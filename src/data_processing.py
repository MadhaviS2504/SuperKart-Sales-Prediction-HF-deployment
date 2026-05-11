import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer

def load_data(filepath='../data/SuperKart (2).csv'):
    """Load the SuperKart dataset from CSV file."""
    return pd.read_csv(filepath)

def preprocess_data(data):
    """Preprocess the data: handle missing values, feature engineering, etc."""
    # Copy data to avoid modifying original
    df = data.copy()

    # Replace 'reg' with 'Regular' in Product_Sugar_Content
    df['Product_Sugar_Content'] = df['Product_Sugar_Content'].replace('reg', 'Regular')

    # Create Store_Age feature
    df['Store_Age'] = df['Store_Establishment_Year'].apply(lambda year: 2026 - year)

    # Drop the original Store_Establishment_Year column
    df.drop('Store_Establishment_Year', axis=1, inplace=True)

    return df

def create_preprocessing_pipeline():
    """Create the preprocessing pipeline for numerical and categorical features."""
    numerical_cols = ['Product_Weight', 'Product_Allocated_Area', 'Product_MRP', 'Store_Age']
    categorical_cols = ['Product_Sugar_Content', 'Product_Type', 'Store_Id', 'Store_Size',
                       'Store_Location_City_Type', 'Store_Type']

    preprocessor = make_column_transformer(
        (make_pipeline(StandardScaler()), numerical_cols),
        (make_pipeline(SimpleImputer(strategy='most_frequent'), OneHotEncoder(handle_unknown='ignore')), categorical_cols)
    )

    return preprocessor

def split_data(X, y, test_size=0.2, val_size=0.25, random_state=1):
    """Split data into train, validation, and test sets."""
    # First split: temporary and test
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # Second split: train and validation
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=val_size, random_state=random_state
    )

    return X_train, X_val, X_test, y_train, y_val, y_test

if __name__ == "__main__":
    # Example usage
    data = load_data('../data/SuperKart (2).csv')
    processed_data = preprocess_data(data)

    X = processed_data.drop(["Product_Store_Sales_Total"], axis=1)
    y = processed_data["Product_Store_Sales_Total"]

    X_train, X_val, X_test, y_train, y_val, y_test = split_data(X, y)

    print(f"Training set shape: {X_train.shape}")
    print(f"Validation set shape: {X_val.shape}")
    print(f"Test set shape: {X_test.shape}")