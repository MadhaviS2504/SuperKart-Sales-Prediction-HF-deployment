import streamlit as st
import requests
import pandas as pd
import json

# --- Configuration ---
# Backend API URL (replace with your deployed backend URL or local URL if running locally)
BACKEND_URL = "http://localhost:7860"  # Update this to your deployed backend URL

st.set_page_config(page_title="Super Kart Sales Prediction", layout="centered")

st.title("🛒 Super Kart Sales Prediction")
st.write("Predict the total sales for products in various Super Kart stores.")

# --- Single Prediction Section ---
st.header("Single Product Sales Prediction")

with st.form("single_prediction_form"):
    st.subheader("Enter Product and Store Details:")

    # Product Features
    product_weight = st.number_input("Product Weight", min_value=1.0, max_value=50.0, value=12.0, step=0.1)
    product_sugar_content = st.selectbox("Product Sugar Content", ['Low Sugar', 'Regular', 'No Sugar'])
    product_allocated_area = st.number_input("Product Allocated Area", min_value=0.001, max_value=0.5, value=0.05, format="%.3f")
    product_type = st.selectbox("Product Type", [
        'Fruits and Vegetables', 'Snack Foods', 'Frozen Foods', 'Dairy',
        'Household', 'Baking Goods', 'Canned', 'Health and Hygiene',
        'Meat', 'Soft Drinks', 'Breads', 'Hard Drinks', 'Others',
        'Starchy Foods', 'Breakfast', 'Seafood'
    ])
    product_mrp = st.number_input("Product MRP (Max Retail Price)", min_value=10.0, max_value=300.0, value=150.0, step=0.1)

    # Store Features
    store_id = st.selectbox("Store ID", ['OUT004', 'OUT001', 'OUT003', 'OUT002'])
    store_size = st.selectbox("Store Size", ['Medium', 'High', 'Small'])
    store_location_city_type = st.selectbox("Store Location City Type", ['Tier 2', 'Tier 1', 'Tier 3'])
    store_type = st.selectbox("Store Type", ['Supermarket Type2', 'Supermarket Type1', 'Departmental Store', 'Food Mart'])
    store_age = st.number_input("Store Age (Years)", min_value=1, max_value=50, value=17)

    submitted_single = st.form_submit_button("Predict Single Sales")

    if submitted_single:
        single_data = {
            "Product_Weight": product_weight,
            "Product_Sugar_Content": product_sugar_content,
            "Product_Allocated_Area": product_allocated_area,
            "Product_Type": product_type,
            "Product_MRP": product_mrp,
            "Store_Id": store_id,
            "Store_Size": store_size,
            "Store_Location_City_Type": store_location_city_type,
            "Store_Type": store_type,
            "Store_Age": store_age
        }

        try:
            response = requests.post(f"{BACKEND_URL}/v1/predictsales", json=single_data)
            if response.status_code == 200:
                result = response.json()
                st.success(f"Predicted Sales Total: ${result['Predicted_Product_Store_Sales_Total']:.2f}")
            else:
                st.error(f"Error from backend: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend API. Please ensure the backend is running and the URL is correct.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# --- Batch Prediction Section ---
st.header("Batch Sales Prediction")
st.write("Upload a CSV file containing multiple product and store entries to get batch predictions.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    try:
        batch_df = pd.read_csv(uploaded_file)
        st.write("Uploaded CSV Preview:")
        st.dataframe(batch_df.head())

        # Prepare the file for sending to the backend
        files = {'file': ('data.csv', batch_df.to_csv(index=False), 'text/csv')}

        if st.button("Predict Batch Sales"):
            try:
                response = requests.post(f"{BACKEND_URL}/v1/batchpredictsales", files=files)
                if response.status_code == 200:
                    result = response.json()
                    st.success("Batch predictions received!")
                    predicted_sales_df = pd.DataFrame({"Predicted_Sales_Total": result['Predicted_Product_Store_Sales_Totals']})
                    st.dataframe(predicted_sales_df)
                else:
                    st.error(f"Error from backend: {response.status_code} - {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend API. Please ensure the backend is running and the URL is correct.")
            except Exception as e:
                st.error(f"An unexpected error occurred during batch prediction: {e}")
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")