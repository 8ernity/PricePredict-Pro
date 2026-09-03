import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import joblib
import json
import os

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "ml_pipeline", "Enhanced_Flat_Price.xlsx")
OUTPUT_DIR = os.path.join(BASE_DIR, "app", "artifacts")
MODEL_PATH = os.path.join(OUTPUT_DIR, "model.pkl")
METADATA_PATH = os.path.join(OUTPUT_DIR, "metadata.json")

def train_model():
    print(f"Loading data from {DATA_PATH}...")
    df = pd.read_excel(DATA_PATH)
    
    # Define features and target
    features = [
        'Area_Sqft', 'Floor', 'Car_Parking_Sqft', 'Bedrooms', 'Facing',
        'City_Tier', 'Property_Type', 'New_Construction', 'Age', 'Furnishing',
        'Bathrooms', 'Balconies', 'Has_Pool', 'Has_Gym', 'Has_Security', 'Has_Backup',
        'City_Preset'
    ]
    X = df[features]
    y = df['Price_Lakh']
    
    print("Building pipeline...")
    # Preprocessing: One-hot encode the categorical variables
    categorical_features = ['Facing', 'City_Tier', 'Property_Type', 'Furnishing', 'City_Preset']
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(drop='first'), categorical_features)
        ],
        remainder='passthrough'
    )
    
    # Create a pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])
    
    print("Training Multiple Linear Regression model...")
    pipeline.fit(X, y)
    
    # --- BUSINESS LOGIC INJECTION ---
    # The raw data has multicollinearity causing parking to get a negative weight.
    # We manually override the Car_Parking_Sqft coefficient to ensure a positive linear scale!
    feature_names = preprocessor.get_feature_names_out()
    parking_idx = list(feature_names).index('remainder__Car_Parking_Sqft')
    # 0.1 Lakhs (10,000 INR) added value per 1 sqft of parking space.
    pipeline.named_steps['regressor'].coef_[parking_idx] = 0.10 
    # --------------------------------
    
    # Save the pipeline
    print(f"Saving model to {MODEL_PATH}...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    
    # Save metadata
    metadata = {
        "model_type": "Multiple Linear Regression",
        "features": features,
        "target": "Price_Lakh",
        "version": "1.0",
        "r2_score": pipeline.score(X, y)
    }
    print(f"Saving metadata to {METADATA_PATH}...")
    with open(METADATA_PATH, 'w') as f:
        json.dump(metadata, f, indent=4)
        
    print(f"Training complete! R2 Score: {metadata['r2_score']:.4f}")

if __name__ == "__main__":
    train_model()
