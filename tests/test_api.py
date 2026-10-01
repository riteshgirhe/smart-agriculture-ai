from fastapi.testclient import TestClient

from backend.app.api.routes import weather
from backend.app.main import app
from backend.app.model_service import MODEL_ARTIFACTS, MODEL_DIR, load_model

client = TestClient(app)


def test_health_reports_model_artifacts():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "AgriSense AI API",
        "models_available": 5,
        "models_total": 5,
    }


def test_crop_prediction_loads_model():
    response = client.post(
        "/api/crop/recommend",
        json={"N": 90, "P": 42, "K": 43, "temperature": 20.88, "humidity": 82.0, "ph": 6.5, "rainfall": 202.9},
    )

    assert response.status_code == 200
    assert response.json()["prediction"] == "rice"
    assert load_model("crop_recommendation_model.pkl") is not None


def test_fertilizer_prediction():
    payload = {
        "Soil_Type": "Clay", "Soil_pH": 6.07, "Soil_Moisture": 34.98, "Organic_Carbon": 0.32,
        "Electrical_Conductivity": 1.87, "Nitrogen_Level": 61, "Phosphorus_Level": 44,
        "Potassium_Level": 84, "Temperature": 19.84, "Humidity": 83.31, "Rainfall": 1693.22,
        "Crop_Type": "Cotton", "Crop_Growth_Stage": "Harvest", "Season": "Kharif",
        "Irrigation_Type": "Canal", "Previous_Crop": "Wheat", "Region": "South",
        "Fertilizer_Used_Last_Season": 297.15, "Yield_Last_Season": 1.19,
    }

    response = client.post("/api/fertilizer/predict", json=payload)

    assert response.status_code == 200
    assert response.json()["prediction"] in {"Compost", "DAP", "MOP", "NPK", "SSP", "Urea", "Zinc Sulphate"}


def test_irrigation_prediction():
    payload = {
        "Soil_Type": "Clay", "Soil_pH": 6.14, "Soil_Moisture": 36.48, "Organic_Carbon": 0.42,
        "Electrical_Conductivity": 2.17, "Temperature_C": 21.9, "Humidity": 31.19,
        "Rainfall_mm": 1167.7, "Sunlight_Hours": 4.01, "Wind_Speed_kmh": 1.97,
        "Crop_Type": "Wheat", "Crop_Growth_Stage": "Vegetative", "Season": "Rabi",
        "Irrigation_Type": "Rainfed", "Water_Source": "Reservoir", "Field_Area_hectare": 4.73,
        "Mulching_Used": "Yes", "Previous_Irrigation_mm": 1.98, "Region": "South",
    }

    response = client.post("/api/irrigation/predict", json=payload)

    assert response.status_code == 200
    assert response.json()["prediction"] in {"High", "Low", "Medium"}


def test_price_prediction():
    payload = {
        "month": "2025-03-01", "commodity_name": "Maize", "state_name": "India", "district_name": "All",
        "avg_min_price": 2191.23, "avg_max_price": 2402.98, "calculationType": "Monthly", "change": -14.43,
    }

    response = client.post("/api/price/predict", json=payload)

    assert response.status_code == 200
    assert isinstance(response.json()["prediction"], (int, float))


def test_yield_prediction():
    payload = {
        "Crop_Type": "Soybean", "Field_Size_hectares": 1.04, "Planting_Date": "2025-06-08",
        "Soil_Type": "Loamy", "Fertilizer_Used": "Urea", "Irrigation_Type": "Furrow/Canal irrigation",
    }

    response = client.post("/api/yield/predict", json=payload)

    assert response.status_code == 200
    assert isinstance(response.json()["prediction"], (int, float))


def test_invalid_input_returns_validation_error():
    response = client.post(
        "/api/crop/recommend",
        json={"N": -1, "P": 42, "K": 43, "temperature": 20, "humidity": 82, "ph": 6.5, "rainfall": 202},
    )

    assert response.status_code == 422


def test_health_identifies_missing_artifact(monkeypatch, tmp_path):
    monkeypatch.setattr("backend.app.main.MODEL_DIR", tmp_path)
    for artifact in list(MODEL_ARTIFACTS.values())[1:]:
        (tmp_path / artifact).touch()

    response = client.get("/health")

    assert response.json()["status"] == "degraded"
    assert response.json()["models_available"] == 4


def test_weather_response_uses_provider_data(monkeypatch):
    current = {
        "name": "Delhi", "sys": {"country": "IN"},
        "main": {"temp": 28.4, "feels_like": 29.1, "humidity": 54},
        "weather": [{"description": "clear sky", "icon": "01d"}], "wind": {"speed": 2.0},
    }
    forecast = {"list": [{"dt": 1790870400, "main": {"temp": 27}, "weather": [{"description": "clear sky", "icon": "01d"}], "pop": 0.2}]}

    monkeypatch.setattr(weather, "_request", lambda endpoint, params: current if endpoint == "weather" else forecast)

    response = client.get("/api/weather?city=Delhi")

    assert response.status_code == 200
    assert response.json()["current"]["temperature"] == 28
    assert response.json()["location"] == "Delhi"


def test_weather_rejects_incomplete_coordinates():
    response = client.get("/api/weather?latitude=28.6")

    assert response.status_code == 422


def test_all_model_artifacts_exist():
    assert all((MODEL_DIR / artifact).is_file() for artifact in MODEL_ARTIFACTS.values())