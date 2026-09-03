import os
import joblib
import pandas as pd
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from datetime import datetime

# ==========================================
# Database Setup
# ==========================================
DATABASE_URL = "sqlite:///./predictions.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PredictionLog(Base):
    __tablename__ = "prediction_logs"
    id = Column(Integer, primary_key=True, index=True)
    area = Column(Float)
    bedrooms = Column(Integer)
    floor = Column(Integer)
    parking = Column(Float)
    facing = Column(String)
    predicted_price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# FastAPI Setup
# ==========================================
app = FastAPI(title="House Price Predictor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the ML Pipeline
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
pipeline = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

class PropertyData(BaseModel):
    area: float
    bedrooms: int
    floor: int
    parking: float
    facing: str
    city_tier: str
    property_type: str
    is_new_construction: bool
    age: int
    furnishing: str
    bathrooms: int
    balconies: int
    city_preset: str
    has_pool: bool
    has_gym: bool
    has_security: bool
    has_backup: bool

@app.post("/predict")
async def predict_price(data: PropertyData, db: Session = Depends(get_db)):
    if pipeline is None:
        return {"error": "Model not loaded on server."}

    # Prepare data for Scikit-Learn
    input_df = pd.DataFrame([{
        'Area_Sqft': data.area,
        'Floor': data.floor,
        'Car_Parking_Sqft': data.parking,
        'Bedrooms': data.bedrooms,
        'Facing': data.facing,
        'City_Tier': data.city_tier,
        'Property_Type': data.property_type,
        'New_Construction': 1 if data.is_new_construction else 0,
        'Age': data.age,
        'Furnishing': data.furnishing,
        'Bathrooms': data.bathrooms,
        'Balconies': data.balconies,
        'City_Preset': data.city_preset,
        'Has_Pool': 1 if data.has_pool else 0,
        'Has_Gym': 1 if data.has_gym else 0,
        'Has_Security': 1 if data.has_security else 0,
        'Has_Backup': 1 if data.has_backup else 0
    }])

    # Predict using the loaded pipeline
    prediction = pipeline.predict(input_df)[0]
    predicted_val = max(0.0, float(prediction))

    # Log to SQLite
    db_log = PredictionLog(
        area=data.area,
        bedrooms=data.bedrooms,
        floor=data.floor,
        parking=data.parking,
        facing=data.facing,
        predicted_price=predicted_val
    )
    db.add(db_log)
    db.commit()

    return {"predicted_price_lakhs": f"{predicted_val:.2f}"}

@app.get("/logs")
def get_logs(db: Session = Depends(get_db), limit: int = 10):
    return db.query(PredictionLog).order_by(PredictionLog.timestamp.desc()).limit(limit).all()
