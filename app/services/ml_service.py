import os
import joblib
import pandas as pd
from app.core.config import MODEL_PATH
from app.schemas.property import PropertyData

class MLService:
    def __init__(self):
        self.pipeline = None
        self.load_model()

    def load_model(self):
        if os.path.exists(MODEL_PATH):
            self.pipeline = joblib.load(MODEL_PATH)
        else:
            print(f"Warning: Model not found at {MODEL_PATH}")

    def predict(self, data: PropertyData) -> float:
        if self.pipeline is None:
            raise ValueError("Model not loaded on server.")

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

        prediction = self.pipeline.predict(input_df)[0]
        return max(0.0, float(prediction))

ml_service = MLService()
