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
OUTPUT_DIR = os.path.join(BASE_DIR, "backend")
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
