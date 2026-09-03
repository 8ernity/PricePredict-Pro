import os

# app/core/config.py is 2 levels deep, so BASE_DIR is app/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

DATABASE_URL = f"sqlite:///{os.path.join(PROJECT_ROOT, 'predictions.db')}"
MODEL_PATH = os.path.join(BASE_DIR, "artifacts", "model.pkl")
