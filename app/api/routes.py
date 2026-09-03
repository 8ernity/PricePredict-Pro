from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from app.db.database import get_db
from app.db.models import PredictionLog
from app.schemas.property import PropertyData
from app.services.ml_service import ml_service

router = APIRouter()

@router.post("/predict")
async def predict_price(data: PropertyData, db: Session = Depends(get_db)):
    try:
        predicted_val = ml_service.predict(data)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Log to SQLite
    db_log = PredictionLog(
        area=data.area,
        bedrooms=data.bedrooms,
        floor=data.floor,
        parking=data.parking,
        facing=data.facing,
        predicted_price=predicted_val,
        city_preset=data.city_preset
    )
    db.add(db_log)
    db.commit()

    return {"predicted_price_lakhs": f"{predicted_val:.2f}"}

@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    # 1. Predictions Made Today
    today = date.today()
    start_of_today = datetime(today.year, today.month, today.day)
    predictions_today = db.query(PredictionLog).filter(
        PredictionLog.timestamp >= start_of_today
    ).count()

    # 2. Avg. Metro Price Searched
    avg_price = db.query(func.avg(PredictionLog.predicted_price)).scalar()
    avg_price_formatted = "₹0.00 Lakhs"
    if avg_price:
        if avg_price >= 100:
            avg_price_formatted = f"₹{(avg_price / 100):.2f} Cr"
        else:
            avg_price_formatted = f"₹{avg_price:.0f} L"
    
    # 3. Most Popular Area (city_preset)
    popular_area = db.query(PredictionLog.city_preset, func.count(PredictionLog.city_preset).label('count')) \
        .group_by(PredictionLog.city_preset) \
        .order_by(func.count(PredictionLog.city_preset).desc()) \
        .first()
    popular_area_name = popular_area[0] if popular_area else "None"

    return {
        "predictions_today": predictions_today,
        "avg_price": avg_price_formatted,
        "popular_area": popular_area_name
    }

@router.get("/logs")
def get_logs(db: Session = Depends(get_db), limit: int = 10):
    return db.query(PredictionLog).order_by(PredictionLog.timestamp.desc()).limit(limit).all()
