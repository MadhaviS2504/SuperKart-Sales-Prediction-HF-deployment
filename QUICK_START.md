# 🚀 Quick Start Guide

Get the SuperKart Sales Prediction system running in **3 steps**!

---

## Step 1️⃣ Train the Model
```bash
cd SuperKart-Sales-Prediction
python train.py
```

**Expected Output:**
```
✓ Loaded 8763 records
✓ Training complete! Model ready for deployment.
```

**Creates:** `models/superkart_sales_prediction_model_v1_0.joblib`

---

## Step 2️⃣ Start Backend API
```bash
cd backend
python app.py
```

**Expected Output:**
```
 * Running on http://127.0.0.1:5000
```

✅ Backend is ready on **http://localhost:5000**

---

## Step 3️⃣ Start Frontend UI (New Terminal)
```bash
cd frontend
streamlit run app.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

✅ Frontend is ready on **http://localhost:8501**

---

## 🎉 You're Done!

Open your browser to **http://localhost:8501** and start making predictions!

### Try a Sample Prediction
Fill in the form:
- Product Weight: 25
- Sugar Content: Regular
- Allocated Area: 0.2
- Product Type: Dairy
- MRP: 200
- Store ID: OUT001
- Store Size: High
- City Type: Tier 1
- Store Type: Supermarket Type1
- Store Age: 5

Click **"Predict"** → See instant sales forecast!

---

## 🐳 Docker (Alternative)

Run everything with Docker Compose:
```bash
docker-compose up -d
```

Then open: **http://localhost:8501**

---

## 📚 Learn More
- **README.md** - Full documentation
- **DEPLOYMENT.md** - Production deployment
- **PROJECT_COMPLETION_SUMMARY.md** - Technical details

---

## ✅ Verify Everything Works
```bash
python verify_project.py
```

Should show: `✓ ALL CHECKS PASSED! Project is ready.`

---

**Questions?** Check [DEPLOYMENT.md](DEPLOYMENT.md#-troubleshooting) troubleshooting section.
