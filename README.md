# SuperKart Sales Prediction

A comprehensive machine learning project for predicting product sales in SuperKart retail stores. This project includes data preprocessing, model training, evaluation, and deployment with both backend API and frontend interface.

## 🏗️ Project Structure

```
SuperKart-Sales-Prediction/
├── data/
│   └── SuperKart (2).csv                 # Dataset
├── src/
│   ├── data_processing.py                # Data loading and preprocessing
│   ├── train_model.py                    # Model training and evaluation
│   └── inference.py                      # Model inference utilities
├── models/
│   └── superkart_sales_prediction_model_v1_0.joblib  # Trained model
├── backend/
│   ├── app.py                            # Flask API
│   ├── requirements.txt                  # Backend dependencies
│   └── Dockerfile                        # Backend Docker configuration
├── frontend/
│   ├── app.py                            # Streamlit web interface
│   ├── requirements.txt                  # Frontend dependencies
│   └── Dockerfile                        # Frontend Docker configuration
├── notebooks/
│   └── Full_Code_SuperKart_Model_Deployment_Project_Notebook (4).ipynb  # Original notebook
├── requirements.txt                      # Main project dependencies
└── README.md                             # Project documentation
```

## 📊 Dataset

The dataset contains information about products and stores with the following features:

- **Product_Id**: Unique identifier of each product
- **Product_Weight**: Weight of each product
- **Product_Sugar_Content**: Sugar content (Low Sugar, Regular, No Sugar)
- **Product_Allocated_Area**: Ratio of allocated display area
- **Product_Type**: Broad category of the product
- **Product_MRP**: Maximum retail price
- **Store_Id**: Unique identifier of each store
- **Store_Establishment_Year**: Year the store was established
- **Store_Size**: Size of the store (High, Medium, Low)
- **Store_Location_City_Type**: Type of city (Tier 1, Tier 2, Tier 3)
- **Store_Type**: Type of store
- **Product_Store_Sales_Total**: Total revenue generated (target variable)

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd SuperKart-Sales-Prediction
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Train the model:
```bash
cd src
python train_model.py
```

## 📈 Model Training

The project uses XGBoost Regressor for sales prediction. The training pipeline includes:

1. **Data Preprocessing**:
   - Handle missing values
   - Feature engineering (Store_Age from Establishment_Year)
   - Standardization of numerical features
   - One-hot encoding of categorical features

2. **Model Training**:
   - Hyperparameter tuning using RandomizedSearchCV
   - Cross-validation for robust evaluation

3. **Model Evaluation**:
   - R-squared, RMSE, MAE, MAPE metrics
   - Train/validation/test split

## 🔧 API Usage

### Backend API

Start the Flask API:

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The API will be available at `http://localhost:7860`

#### Single Prediction

```python
import requests

data = {
    "Product_Weight": 12.0,
    "Product_Sugar_Content": "Regular",
    "Product_Allocated_Area": 0.05,
    "Product_Type": "Snack Foods",
    "Product_MRP": 150.0,
    "Store_Id": "OUT004",
    "Store_Size": "Medium",
    "Store_Location_City_Type": "Tier 2",
    "Store_Type": "Supermarket Type2",
    "Store_Age": 17
}

response = requests.post("http://localhost:7860/v1/predictsales", json=data)
print(response.json())
```

#### Batch Prediction

```python
import pandas as pd

# Load your CSV file
df = pd.read_csv("your_data.csv")
files = {'file': ('data.csv', df.to_csv(index=False), 'text/csv')}

response = requests.post("http://localhost:7860/v1/batchpredictsales", files=files)
print(response.json())
```

### Frontend Interface

Start the Streamlit app:

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

The web interface will be available at `http://localhost:8501`

## 🐳 Docker Deployment

### Backend

```bash
cd backend
docker build -t superkart-backend .
docker run -p 7860:7860 superkart-backend
```

### Frontend

```bash
cd frontend
docker build -t superkart-frontend .
docker run -p 8501:8501 superkart-frontend
```

## 📊 Model Performance

The tuned XGBoost model achieves:
- **R-squared**: ~0.92 on test data
- **RMSE**: ~302
- **MAE**: ~136
- **MAPE**: ~0.046

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Dataset and problem statement from SuperKart retail chain
- Built as part of Model Deployment module
- Uses XGBoost for robust regression modeling