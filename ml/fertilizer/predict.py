import joblib
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
model = joblib.load(project_root / "backend" / "app" / "models" / "fertilizer_model.pkl")
new_data = pd.DataFrame([{
    "Soil_Type": "Clay", "Soil_pH": 6.07, "Soil_Moisture": 34.98,
    "Organic_Carbon": .32, "Electrical_Conductivity": 1.87, "Nitrogen_Level": 61,
    "Phosphorus_Level": 44, "Potassium_Level": 84, "Temperature": 19.84,
    "Humidity": 83.31, "Rainfall": 1693.22, "Crop_Type": "Cotton",
    "Crop_Growth_Stage": "Harvest", "Season": "Kharif", "Irrigation_Type": "Canal",
    "Previous_Crop": "Wheat", "Region": "South", "Fertilizer_Used_Last_Season": 297.15,
    "Yield_Last_Season": 1.19,
}])
print(f"Recommended Fertilizer: {model.predict(new_data)[0]}")
