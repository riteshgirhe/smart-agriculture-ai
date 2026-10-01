import joblib
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
model = joblib.load(project_root / "backend" / "app" / "models" / "irrigation_model.pkl")
new_data = pd.DataFrame([{
    "Soil_Type": "Clay", "Soil_pH": 6.14, "Soil_Moisture": 36.48,
    "Organic_Carbon": .42, "Electrical_Conductivity": 2.17, "Temperature_C": 21.9,
    "Humidity": 31.19, "Rainfall_mm": 1167.7, "Sunlight_Hours": 4.01,
    "Wind_Speed_kmh": 1.97, "Crop_Type": "Wheat", "Crop_Growth_Stage": "Vegetative",
    "Season": "Rabi", "Irrigation_Type": "Rainfed", "Water_Source": "Reservoir",
    "Field_Area_hectare": 4.73, "Mulching_Used": "Yes", "Previous_Irrigation_mm": 1.98,
    "Region": "South",
}])
print(f"Irrigation Need: {model.predict(new_data)[0]}")
