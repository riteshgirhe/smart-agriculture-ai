import joblib
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
model = joblib.load(project_root / "backend" / "app" / "models" / "price_prediction_model.pkl")
new_data = pd.DataFrame([{
    "month": 3, "commodity_name": "Maize", "avg_min_price": 2191.23,
    "avg_max_price": 2402.98, "state_name": "India", "district_name": "All",
    "calculationType": "Monthly", "change": -14.43,
}])
print(f"Predicted Modal Price: {model.predict(new_data)[0]:.2f}")
