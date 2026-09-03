import pandas as pd
import numpy as np
import os

# Paths
DATA_PATH = "D:/Downloads/Flat_Price_Multiple_Linear_Regression_100.xlsx"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(BASE_DIR, "ml_pipeline", "Enhanced_Flat_Price.xlsx")

def generate_mock_data():
    print(f"Loading original data from {DATA_PATH}...")
    df = pd.read_excel(DATA_PATH)
    
    np.random.seed(42)  # For reproducibility
    
    n_rows = len(df)
    
    # 1. City Tier
    df['City_Tier'] = np.random.choice(['Metro', 'Tier-2', 'Tier-3'], n_rows, p=[0.5, 0.3, 0.2])
    
    # 1.5 City Preset
    presets = [
        "Custom Input",
        "Mumbai",
        "Bengaluru",
        "Delhi NCR",
        "Hyderabad",
        "Pune",
        "Kolkata",
        "Chennai"
    ]
    df['City_Preset'] = np.random.choice(presets, n_rows, p=[0.6, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.1])
    
    # 2. Property Type
    df['Property_Type'] = np.random.choice(['Apartment', 'Villa', 'Independent'], n_rows, p=[0.7, 0.15, 0.15])
    
    # 3. New Construction
    df['New_Construction'] = np.random.choice([0, 1], n_rows, p=[0.7, 0.3])
    
    # 4. Property Age
    # If new construction, age is 0, else 1 to 50
    df['Age'] = df['New_Construction'].apply(lambda x: 0 if x == 1 else np.random.randint(1, 51))
    
    # 5. Furnishing
    df['Furnishing'] = np.random.choice(['Unfurnished', 'Semi-Furnished', 'Fully-Furnished'], n_rows, p=[0.2, 0.5, 0.3])
    
    # 6. Bathrooms and Balconies
    # Bathrooms usually proportional to Bedrooms (from 1 to Bedrooms + 1)
    df['Bathrooms'] = df['Bedrooms'].apply(lambda b: np.random.randint(max(1, b-1), b+2))
    df['Balconies'] = df['Bedrooms'].apply(lambda b: np.random.randint(0, min(b, 4)))
    
    # 7. Premium Amenities
    df['Has_Pool'] = np.random.choice([0, 1], n_rows, p=[0.6, 0.4])
    df['Has_Gym'] = np.random.choice([0, 1], n_rows, p=[0.5, 0.5])
    df['Has_Security'] = np.random.choice([0, 1], n_rows, p=[0.2, 0.8])
    df['Has_Backup'] = np.random.choice([0, 1], n_rows, p=[0.3, 0.7])
    
    # VILLA OVERRIDES (Villas usually have these)
    df.loc[df['Property_Type'] == 'Villa', 'Has_Security'] = 1
    df.loc[df['Property_Type'] == 'Villa', 'Has_Backup'] = 1
    
    print("Adjusting Price_Lakh to logically correlate with new features...")
    # Add pricing logic based on synthetic features so the ML model can learn it
    # We don't overwrite completely, we just add to the original price to keep original relationships intact.
    
    # Base adjustments
    tier_adj = {'Metro': 30, 'Tier-2': 10, 'Tier-3': 0}
    type_adj = {'Apartment': 0, 'Independent': 20, 'Villa': 40}
    furnish_adj = {'Unfurnished': 0, 'Semi-Furnished': 5, 'Fully-Furnished': 15}
    
    preset_adj = {
        "Custom Input": 0,
        "Mumbai": 150,
        "Bengaluru": 80,
        "Delhi NCR": 90,
        "Hyderabad": 60,
        "Pune": 50,
        "Kolkata": 35,
        "Chennai": 40
    }
    
    df['Price_Lakh'] = df['Price_Lakh'] + \
                       df['City_Tier'].map(tier_adj) + \
                       df['City_Preset'].map(preset_adj) + \
                       df['Property_Type'].map(type_adj) + \
                       (df['New_Construction'] * 10) + \
                       (df['Age'] * -0.5) + \
                       df['Furnishing'].map(furnish_adj) + \
                       (df['Bathrooms'] * 4) + \
                       (df['Balconies'] * 2) + \
                       (df['Has_Pool'] * 5) + \
                       (df['Has_Gym'] * 3) + \
                       (df['Has_Security'] * 2) + \
                       (df['Has_Backup'] * 2)
                       
    # Ensure price isn't negative (edge cases)
    df['Price_Lakh'] = df['Price_Lakh'].apply(lambda x: max(10, x))
    
    print(f"Saving enhanced dataset to {OUTPUT_PATH}...")
    df.to_excel(OUTPUT_PATH, index=False)
    print("Success!")

if __name__ == "__main__":
    generate_mock_data()
