from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from app.db.database import Base

class PredictionLog(Base):
    __tablename__ = "prediction_logs"
    id = Column(Integer, primary_key=True, index=True)
    area = Column(Float)
    bedrooms = Column(Integer)
    floor = Column(Integer)
    parking = Column(Float)
    facing = Column(String)
    predicted_price = Column(Float)
    city_preset = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
