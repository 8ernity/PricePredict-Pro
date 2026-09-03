# PricePredict Pro 🏡

A modern, highly-interactive web application that leverages machine learning to predict house prices across various cities in India. The application features a sleek Glassmorphism UI, a dynamic interactive Leaflet map, and a responsive design powered by Vanilla HTML, CSS, JavaScript, and Tailwind CSS, coupled with a robust FastAPI backend.

## ✨ Features

- **Interactive Map:** Click on any tier-1 or tier-2 Indian city in the sidebar, and watch the map dynamically fly to that location using Leaflet.js.
- **Machine Learning Integration:** Uses a Multiple Linear Regression (MLR) model built with Scikit-learn to estimate property values based on location, area, and configuration (BHK).
- **Modern UI:** Features a high-quality Glassmorphism dark theme, interactive shiny CTA buttons, and a responsive layout using Tailwind CSS.
- **FastAPI Backend:** A blazing-fast backend API providing endpoints for model inference and dynamic data fetching.

## 🚀 Tech Stack

- **Frontend:** Vanilla HTML5, CSS3, JavaScript, Tailwind CSS, Leaflet.js
- **Backend:** Python, FastAPI, Uvicorn
- **Machine Learning:** Scikit-learn, Pandas, Joblib
- **Database:** SQLite (Stores historical prediction data)

## 📁 Project Structure

```text
PricePredict-Pro/
├── backend/
│   ├── main.py                # FastAPI application & API endpoints
│   ├── metadata.json          # Model metadata (categories, cities, etc.)
│   ├── model.pkl              # Serialized MLR model
│   ├── predictions.db         # SQLite database for storing predictions
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── css/
│   │   └── style.css          # Custom styles & Tailwind overrides
│   ├── js/
│   │   └── script.js          # Frontend logic and API integration
│   └── index.html             # Main dashboard UI
└── ml_pipeline/
    ├── generate_mock_data.py  # Script to generate synthetic dataset
    ├── train_model.py         # Script to train and save the ML model
    └── Enhanced_Flat_Price.xlsx # Generated dataset
```

## 🛠️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/8ernity/PricePredict-Pro.git
cd PricePredict-Pro
```

### 2. Setup the Backend
Navigate to the backend directory and install the required Python packages. We recommend using a virtual environment.
```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Run the ML Pipeline (Optional)
If you want to re-train the model or generate new mock data:
```bash
cd ../ml_pipeline
python generate_mock_data.py
python train_model.py
```

### 4. Start the API Server
Return to the backend directory and start the FastAPI server:
```bash
cd ../backend
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### 5. Run the Frontend
You can simply open `frontend/index.html` in your favorite browser, or serve it using any local HTTP server (like VS Code Live Server or Python's HTTP module).
```bash
cd ../frontend
python -m http.server 3000
```
Visit `http://localhost:3000` to view the application!

## 📜 License

This project is open-source and available under the MIT License.
