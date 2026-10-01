# make the predictions

# import necessary libraries
import pandas as pd
import joblib
from pathlib import Path

# load the trained model
project_root = Path(__file__).resolve().parents[2]
model_path = project_root / "backend" / "app" / "models" / "random_forest_model.pkl"
model = joblib.load(model_path)

# new data for prediction
new_data = pd.DataFrame({
    "Crop Type": ["Rice"],
    "Soil Type": ["Clay"],
    "Fertilizer Used": ["Yes"],
    "Irrigation Type": ["Drip"],
    "Field Size (hectares)": [2.5],
    "Planting_Year": [2023],
    "Planting_Month": [5],
    "Planting_Day": [15],
    "Planting_DayOfYear": [135],
    "Planting_Quarter": [2],
})

# make predictions
predictions = model.predict(new_data)

# print the predictions
print(f"Predicted Yield: {predictions[0]}")