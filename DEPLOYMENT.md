# SuperKart Sales Prediction - Deployment Guide

## ✅ Project Status
- **Model Training**: ✓ Complete (Random Forest with 92.6% R²)
- **Backend API**: ✓ Ready (Flask with Gunicorn)
- **Frontend UI**: ✓ Ready (Streamlit)
- **Docker**: ✓ Configured
- **Documentation**: ✓ Complete

---

## 🚀 Quick Start (Local Development)

### Prerequisites
```bash
# Python 3.9+
python --version

# Dependencies already installed
pip list | grep -E "pandas|scikit-learn|flask|streamlit"
```

### 1. Train the Model (One-time setup)
```bash
cd SuperKart-Sales-Prediction
python train.py
```

**Output:**
- Trained Random Forest model: `models/superkart_sales_prediction_model_v1_0.joblib`
- Performance: R² = 0.926, RMSE = 291.75, MAE = 111.40

### 2. Start Backend API (Terminal 1)
```bash
cd backend
python app.py
```

**Output:**
```
 * Running on http://127.0.0.1:5000
```

**Available Endpoints:**
- `GET /` - Welcome message
- `POST /v1/predictsales` - Single prediction
- `POST /v1/batchpredictsales` - Batch predictions from CSV

### 3. Start Frontend UI (Terminal 2)
```bash
cd frontend
streamlit run app.py
```

**Output:**
```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

### Test Single Prediction via API
```bash
curl -X POST http://localhost:5000/v1/predictsales \
  -H "Content-Type: application/json" \
  -d '{
    "Product_Weight": 20.5,
    "Product_Sugar_Content": "Low Sugar",
    "Product_Allocated_Area": 0.2,
    "Product_Type": "Snack Foods",
    "Product_MRP": 150.0,
    "Store_Id": "OUT001",
    "Store_Size": "High",
    "Store_Location_City_Type": "Tier 1",
    "Store_Type": "Supermarket Type1",
    "Store_Age": 5
  }'
```

**Response:**
```json
{
  "Predicted_Product_Store_Sales_Total": 1250.45
}
```

---

## 🐳 Docker Deployment

### Build Images
```bash
# Build backend image
cd backend
docker build -t superkart-api:latest .

# Build frontend image
cd frontend
docker build -t superkart-ui:latest .
```

### Run with Docker Compose
Create `docker-compose.yml` in project root:
```yaml
version: '3.8'

services:
  backend:
    image: superkart-api:latest
    ports:
      - "7860:7860"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./models:/app/models:ro
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:7860/"]
      interval: 10s
      timeout: 5s
      retries: 3

  frontend:
    image: superkart-ui:latest
    ports:
      - "8501:8501"
    environment:
      - BACKEND_URL=http://backend:7860
    depends_on:
      - backend
```

### Start Services
```bash
docker-compose up -d
```

**Access:**
- Frontend UI: http://localhost:8501
- Backend API: http://localhost:7860

---

## 📊 Model Performance

**Random Forest Regressor (Selected Model)**
| Metric | Value |
|--------|-------|
| R² Score | 0.926 |
| Adjusted R² | 0.926 |
| RMSE | 291.75 |
| MAE | 111.40 |
| MAPE | 3.93% |

**Dataset Split:**
- Training: 5,257 samples (60%)
- Validation: 1,753 samples (20%)
- Testing: 1,753 samples (20%)

---

## 🔧 Configuration

### Backend Configuration
**File:** `backend/app.py`

```python
# Model path
model = joblib.load("../models/superkart_sales_prediction_model_v1_0.joblib")

# Flask port (Gunicorn in production)
app.run(host='0.0.0.0', port=5000, debug=False)
```

### Frontend Configuration
**File:** `frontend/app.py`

```python
# Backend URL for API calls
BACKEND_URL = "http://localhost:7860"

# For cloud deployment, update to:
BACKEND_URL = "https://your-api-domain.com"
```

---

## 📁 Project Structure

```
SuperKart-Sales-Prediction/
├── data/
│   └── SuperKart (2).csv           # Original dataset (8,763 records)
├── src/
│   ├── data_processing.py          # Data pipeline
│   ├── train_model.py              # ML training
│   └── inference.py                # Prediction utilities
├── models/
│   └── superkart_sales_prediction_model_v1_0.joblib
├── backend/
│   ├── app.py                      # Flask REST API
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app.py                      # Streamlit UI
│   ├── requirements.txt
│   └── Dockerfile
├── notebooks/
│   └── Full_Code_SuperKart_Model_Deployment_Project_Notebook.ipynb
├── train.py                        # Training wrapper
├── requirements.txt                # All dependencies
├── README.md                       # Main documentation
├── DEPLOYMENT.md                   # This file
└── .gitignore
```

---

## 🌐 Cloud Deployment

### Deploy to Hugging Face Spaces

1. **Create Space:**
   - Visit https://huggingface.co/spaces
   - Create Docker Space with your repo

2. **Update Frontend Config:**
   ```python
   BACKEND_URL = "https://username-superkart-api.hf.space"
   ```

3. **Push Repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

### Deploy to AWS/GCP/Azure

1. **Containerize Application:**
   ```bash
   docker-compose build
   docker tag superkart-api:latest your-registry/superkart-api:latest
   docker push your-registry/superkart-api:latest
   ```

2. **Deploy with Kubernetes/App Service**
3. **Update BACKEND_URL in frontend**

---

## 🐛 Troubleshooting

### Model File Not Found
```
Error: FileNotFoundError: models/superkart_sales_prediction_model_v1_0.joblib
```
**Solution:** Run `python train.py` from project root

### Backend Connection Failed
```
Error: ConnectionError: Connection refused at 0.0.0.0:7860
```
**Solution:** Ensure backend is running: `cd backend && python app.py`

### XGBoost Import Error
```
ModuleNotFoundError: No module named 'xgboost'
```
**Solution:** Model falls back to Random Forest automatically (still performs well at R² = 0.926)

### Streamlit "API Unavailable"
```
Error: Connection refused - Backend not responding
```
**Solution:** 
- Check backend is running on port 5000/7860
- Update `BACKEND_URL` in `frontend/app.py` to match backend address

---

## 📝 API Documentation

### Single Prediction Endpoint

**Request:**
```
POST /v1/predictsales
Content-Type: application/json

{
  "Product_Weight": 25.0,
  "Product_Sugar_Content": "Regular",
  "Product_Allocated_Area": 0.15,
  "Product_Type": "Dairy",
  "Product_MRP": 200.0,
  "Store_Id": "OUT002",
  "Store_Size": "Medium",
  "Store_Location_City_Type": "Tier 2",
  "Store_Type": "Supermarket Type2",
  "Store_Age": 8
}
```

**Response:**
```json
{
  "Predicted_Product_Store_Sales_Total": 1180.35
}
```

### Batch Prediction Endpoint

**Request:**
```
POST /v1/batchpredictsales
Content-Type: multipart/form-data

[File: predictions.csv with columns matching single prediction]
```

**Response:**
```json
{
  "Predicted_Product_Store_Sales_Totals": [1180.35, 950.20, 1520.10]
}
```

---

## 📊 Monitoring & Logs

### Backend Logs
```bash
# Run with verbose logging
cd backend
python app.py 2>&1 | tee backend.log
```

### Frontend Logs
```bash
# View Streamlit logs
cd frontend
streamlit run app.py --logger.level=debug 2>&1 | tee frontend.log
```

### Docker Logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

---

## ✨ Next Steps

1. **GitHub Setup:** Push to GitHub for version control
2. **CI/CD Pipeline:** Set up automated testing with GitHub Actions
3. **Model Monitoring:** Track prediction performance in production
4. **A/B Testing:** Compare models if you retrain with XGBoost
5. **Scaling:** Consider load balancing for high-traffic scenarios

---

## 📞 Support

For issues or questions:
1. Check README.md for dataset details
2. Review inline code comments
3. Check logs for error details
4. Verify all dependencies: `pip install -r requirements.txt`

---

**Last Updated:** 2026-05-11
**Model Version:** v1.0 (Random Forest)
**Status:** Production Ready ✓
