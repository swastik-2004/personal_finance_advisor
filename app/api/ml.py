from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import numpy as np
from sklearn.ensemble import IsolationForest

from app.db.session import get_db
from app.models.transaction import Transaction
from app.models.user import User
from app.auth import get_current_user
from ml.predict import predict_category, forecast_spending

router=APIRouter()

@router.get("/predict/category")
async def predict_expense_category(amount: float, current_user: User = Depends(get_current_user)):
    try:
        category = predict_category(amount)
        return {"amount": amount, "predicted_category": category}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/predict/forecast")
async def forecast_monthly_spending(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result=await db.execute(
        select(Transaction).where(Transaction.user_id == current_user.id))
    transactions = result.scalars().all()
    if not transactions:
        raise HTTPException(status_code=400, detail="No transactions found to forecast")
    
    expenses = [t for t in transactions if t.transaction_type == "expense"]
    if not expenses:
        raise HTTPException(status_code=400, detail="No expense transactions found to forecast")
    data=[{"amount":float(t.amount), "date": t.date} for t in expenses]
    try:
        forecast = forecast_spending(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forecast error: {str(e)}")
    return {"predicted_monthly_spending": round(forecast, 2)}

@router.get("/predicted/anomalies")
async def check_anomalies(
    db:AsyncSession = Depends(get_db),
    current_user:User = Depends(get_current_user)
):
    result = await db.execute(
        select(Transaction).where(Transaction.user_id == current_user.id)
    )
    transactions = result.scalars().all()

    expenses = [t for t in transactions if t.transaction_type == "expense"]
    if len(expenses) < 3:
        return {"anomalies": [], "total_flagged": 0}

    amounts = np.array([float(t.amount) for t in expenses]).reshape(-1, 1)
    clf = IsolationForest(contamination=0.2, random_state=42)
    preds = clf.fit_predict(amounts)

    flagged = [
        {"id": t.id, "amount": float(t.amount), "description": t.description}
        for t, pred in zip(expenses, preds) if pred == -1
    ]
    return {"anomalies": flagged, "total_flagged": len(flagged)}

    