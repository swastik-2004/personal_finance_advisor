import pandas as pd
import joblib
import os

MODEL_DIR=os.path.join( os.path.dirname(__file__), 'models')    

def load_model(name):
    path=os.path.join(MODEL_DIR, name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file {name} not found in {MODEL_DIR}")
    return joblib.load(path)

def predict_category(description: str) -> str:
    model = load_model("classifier.pkl")
    return model.predict([description.lower()])[0]

def forecast_spending(transactions: list[dict])->float:
    if not transactions:
        return 0.0
    df=pd.DataFrame(transactions)
    df["date"]=pd.to_datetime(df["date"])
    df["month"]=df["date"].dt.to_period("M")
    monthly=df.groupby("month")["amount"].sum()
    return float(monthly.mean())