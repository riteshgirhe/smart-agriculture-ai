import joblib
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
model = joblib.load(project_root / "backend" / "app" / "models" / "crop_recommendation_model.pkl")
new_data = pd.DataFrame([{
    "N": 90, "P": 42, "K": 43, "temperature": 20.8,
    "humidity": 82, "ph": 6.5, "rainfall": 202.9,
}])
print(f"Recommended Crop: {model.predict(new_data)[0]}")
