import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier

MODEL_DIR=os.path.join( os.path.dirname(__file__), 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

CATEGORIES=["Food","Rent", "Travel", "Shopping", "Health", "Entertainment", "Utilities", "Other"]

def train_classifier(df: pd.DataFrame):
    df=df[df["category"].isin(CATEGORIES)].copy()
    le=LabelEncoder()
    df["category_encoded"]=le.fit_transform(df["category"])

    X=df[["amount"]].values
    y=df["category_encoded"].values

    model=XGBClassifier(n_estimators=100,random_state=42)
    model.fit(X,y)

    joblib.dump(model,os.path.join(MODEL_DIR,"classifier.pkl"))
    joblib.dump(le, os.path.join(MODEL_DIR, "label_encoder.pkl"))
    print("Classifier trained and saved.")

def train_anomaly_detector(df: pd.DataFrame):
    X=df[["amount"]].values
    model=IsolationForest(contamination=0.01, random_state=42)
    model.fit(X)
    joblib.dump(model, os.path.join(MODEL_DIR, "anomaly_detector.pkl"))
    print("Anomaly detector trained and saved.")

def train_all(df:pd.DataFrame):
    train_classifier(df)
    train_anomaly_detector(df)

if __name__ == "__main__":
    sample_data = pd.DataFrame({
        "amount": [200, 1500, 800, 50, 300, 120, 900, 60, 250, 1800],
        "category": ["Food", "Rent", "Travel", "Food", "Shopping", "Health", "Rent", "Food", "Entertainment", "Rent"]
    })
    train_all(sample_data)
