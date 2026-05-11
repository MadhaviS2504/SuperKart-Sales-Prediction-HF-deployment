import sys
import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.pipeline import make_pipeline
from sklearn import metrics
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
import joblib

try:
    from xgboost import XGBRegressor
except ImportError:
    print("XGBoost not found. Using RandomForest instead.")
    XGBRegressor = None

# Add src to path for imports
sys.path.insert(0, os.path.dirname(__file__))
from data_processing import load_data, preprocess_data, create_preprocessing_pipeline, split_data

def adj_r2_score(predictors, targets, predictions):
    """Compute adjusted R-squared."""
    r2 = r2_score(targets, predictions)
    n = predictors.shape[0]
    k = predictors.shape[1]
    return 1 - ((1 - r2) * (n - 1) / (n - k - 1))

def model_performance_regression(model, predictors, target):
    """Compute different metrics for regression model performance."""
    pred = model.predict(predictors)

    r2 = r2_score(target, pred)
    adjr2 = adj_r2_score(predictors, target, pred)
    rmse = np.sqrt(mean_squared_error(target, pred))
    mae = mean_absolute_error(target, pred)
    mape = mean_absolute_percentage_error(target, pred)

    df_perf = pd.DataFrame({
        "RMSE": rmse,
        "MAE": mae,
        "R-squared": r2,
        "Adj. R-squared": adjr2,
        "MAPE": mape,
    }, index=[0])

    return df_perf

def train_random_forest(X_train, y_train, tune=False):
    """Train Random Forest model with optional hyperparameter tuning."""
    preprocessor = create_preprocessing_pipeline()
    rf_model = RandomForestRegressor(random_state=42)
    rf_pipeline = make_pipeline(preprocessor, rf_model)

    if tune:
        parameters = {
            'randomforestregressor__max_depth': [3, 4, 5, 6],
            'randomforestregressor__max_features': ['sqrt', 'log2', None],
            'randomforestregressor__n_estimators': [50, 75, 100, 125, 150]
        }

        scorer = metrics.make_scorer(metrics.r2_score)
        grid_obj = RandomizedSearchCV(rf_pipeline, parameters, n_iter=50, scoring=scorer, cv=5, random_state=42)
        grid_obj = grid_obj.fit(X_train, y_train)
        rf_tuned = grid_obj.best_estimator_
        return rf_tuned

    rf_pipeline.fit(X_train, y_train)
    return rf_pipeline

def train_xgboost(X_train, y_train, tune=False):
    """Train XGBoost model with optional hyperparameter tuning."""
    if XGBRegressor is None:
        print("XGBoost not available. Please install xgboost.")
        return None
    
    preprocessor = create_preprocessing_pipeline()
    xgb_model = XGBRegressor(random_state=42, verbosity=0)
    xgb_pipeline = make_pipeline(preprocessor, xgb_model)

    if tune:
        from scipy.stats import randint, uniform
        param_dist = {
            'xgbregressor__n_estimators': randint(50, 200),
            'xgbregressor__max_depth': randint(2, 5),
            'xgbregressor__colsample_bytree': uniform(0.4, 0.3),
            'xgbregressor__colsample_bylevel': uniform(0.4, 0.3),
            'xgbregressor__learning_rate': uniform(0.01, 0.1),
            'xgbregressor__reg_lambda': uniform(0.4, 0.3),
        }

        scorer = metrics.make_scorer(metrics.r2_score)
        grid_obj = RandomizedSearchCV(xgb_pipeline, param_dist, n_iter=100, scoring=scorer, cv=5,
                                    random_state=42, n_jobs=-1, verbose=1)
        grid_obj = grid_obj.fit(X_train, y_train)
        xgb_tuned = grid_obj.best_estimator_
        return xgb_tuned

    xgb_pipeline.fit(X_train, y_train)
    return xgb_pipeline

def save_model(model, filepath):
    """Save the trained model to disk."""
    joblib.dump(model, filepath)
    print(f"Model saved to {filepath}")

def load_model(filepath):
    """Load a trained model from disk."""
    return joblib.load(filepath)

if __name__ == "__main__":
    try:
        # Load and preprocess data
        print("Loading data...")
        data = load_data('../data/SuperKart (2).csv')
        processed_data = preprocess_data(data)

        X = processed_data.drop(["Product_Store_Sales_Total"], axis=1)
        y = processed_data["Product_Store_Sales_Total"]

        print("Splitting data...")
        X_train, X_val, X_test, y_train, y_val, y_test = split_data(X, y)

        # Train models (disable tuning for quick demo)
        print("Training Random Forest...")
        rf_model = train_random_forest(X_train, y_train, tune=False)

        print("Training XGBoost...")
        xgb_model = train_xgboost(X_train, y_train, tune=False)

        # Evaluate models
        print("\nRandom Forest Test Performance:")
        if rf_model:
            rf_perf = model_performance_regression(rf_model, X_test, y_test)
            print(rf_perf)

        print("\nXGBoost Test Performance:")
        if xgb_model:
            xgb_perf = model_performance_regression(xgb_model, X_test, y_test)
            print(xgb_perf)
            
            # Save the best model (XGBoost based on notebook results)
            print("\nSaving model...")
            save_model(xgb_model, '../models/superkart_sales_prediction_model_v1_0.joblib')
        else:
            # Fallback to Random Forest if XGBoost not available
            print("\nSaving Random Forest model as fallback...")
            save_model(rf_model, '../models/superkart_sales_prediction_model_v1_0.joblib')
            
    except Exception as e:
        print(f"Error during training: {e}")
        import traceback
        traceback.print_exc()