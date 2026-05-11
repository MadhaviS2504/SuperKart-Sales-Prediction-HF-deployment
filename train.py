#!/usr/bin/env python3
"""
Script to train the SuperKart sales prediction model.
Run this from the project root directory.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from data_processing import load_data, preprocess_data, split_data
    from train_model import train_random_forest, train_xgboost, model_performance_regression, save_model
    
    print("=" * 60)
    print("SuperKart Sales Prediction - Model Training Pipeline")
    print("=" * 60)
    
    print("\n[1/6] Loading data...")
    data = load_data('data/SuperKart (2).csv')
    print(f"    ✓ Loaded {len(data)} records with {len(data.columns)} features")
    
    print("\n[2/6] Preprocessing data...")
    processed_data = preprocess_data(data)
    print(f"    ✓ Preprocessing complete")

    X = processed_data.drop(["Product_Store_Sales_Total"], axis=1)
    y = processed_data["Product_Store_Sales_Total"]
    print(f"    ✓ Features: {X.shape[1]}, Target shape: {y.shape}")

    print("\n[3/6] Splitting data into train/val/test...")
    X_train, X_val, X_test, y_train, y_val, y_test = split_data(X, y)
    print(f"    ✓ Train: {X_train.shape[0]}, Val: {X_val.shape[0]}, Test: {X_test.shape[0]}")

    print("\n[4/6] Training Random Forest Regressor...")
    rf_model = train_random_forest(X_train, y_train, tune=False)
    print("    ✓ Random Forest training complete")

    print("\n[5/6] Training XGBoost Regressor...")
    try:
        xgb_model = train_xgboost(X_train, y_train, tune=False)
        if xgb_model is None:
            print("    ✗ XGBoost unavailable - will use Random Forest")
            xgb_model = None
        else:
            print("    ✓ XGBoost training complete")
    except Exception as e:
        print(f"    ✗ XGBoost training failed: {e}")
        print("    → Using Random Forest as fallback")
        xgb_model = None

    print("\n[6/6] Evaluating and saving models...")
    
    print("\n  Random Forest Test Performance:")
    rf_perf = model_performance_regression(rf_model, X_test, y_test)
    print(rf_perf.to_string(index=False))

    if xgb_model is not None:
        print("\n  XGBoost Test Performance:")
        xgb_perf = model_performance_regression(xgb_model, X_test, y_test)
        print(xgb_perf.to_string(index=False))
        
        # Save XGBoost (better performance)
        save_model(xgb_model, 'models/superkart_sales_prediction_model_v1_0.joblib')
        print("\n    ✓ XGBoost model saved to models/superkart_sales_prediction_model_v1_0.joblib")
    else:
        # Save Random Forest fallback
        save_model(rf_model, 'models/superkart_sales_prediction_model_v1_0.joblib')
        print("\n    ✓ Random Forest model saved to models/superkart_sales_prediction_model_v1_0.joblib")
    
    print("\n" + "=" * 60)
    print("Training complete! Model ready for deployment.")
    print("=" * 60)

except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("Make sure all dependencies are installed:")
    print("  pip install -r requirements.txt")
    sys.exit(1)
except FileNotFoundError as e:
    print(f"\n❌ File Error: {e}")
    print("Check that you're running from the project root directory:")
    print("  cd SuperKart-Sales-Prediction")
    print("  python train.py")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error during training: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)