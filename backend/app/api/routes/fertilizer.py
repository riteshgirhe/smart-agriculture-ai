from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal

from ...model_service import predict_safely

router = APIRouter(prefix="/api/fertilizer", tags=["fertilizer"])


class FertilizerRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    Soil_Type: Literal["Clay", "Loamy", "Sandy", "Silt"]
    Soil_pH: float = Field(ge=0, le=14)
    Soil_Moisture: float = Field(ge=0, le=100)
    Organic_Carbon: float = Field(ge=0, le=10)
    Electrical_Conductivity: float = Field(ge=0, le=100)
    Nitrogen_Level: float = Field(ge=0, le=10000)
    Phosphorus_Level: float = Field(ge=0, le=10000)
    Potassium_Level: float = Field(ge=0, le=10000)
    Temperature: float = Field(ge=-20, le=60)
    Humidity: float = Field(ge=0, le=100)
    Rainfall: float = Field(ge=0, le=10000)
    Crop_Type: Literal["Cotton", "Maize", "Potato", "Rice", "Sugarcane", "Tomato", "Wheat"]
    Crop_Growth_Stage: Literal["Flowering", "Harvest", "Sowing", "Vegetative"]
    Season: Literal["Kharif", "Rabi", "Zaid"]
    Irrigation_Type: Literal["Canal", "Drip", "Rainfed", "Sprinkler"]
    Previous_Crop: Literal["Cotton", "Maize", "Potato", "Rice", "Sugarcane", "Tomato", "Wheat"]
    Region: Literal["Central", "East", "North", "South", "West"]
    Fertilizer_Used_Last_Season: float = Field(ge=0, le=10000)
    Yield_Last_Season: float = Field(ge=0, le=100)


@router.post("/predict")
def predict_fertilizer(request: FertilizerRequest) -> dict[str, Any]:
    return predict_safely("fertilizer_model.pkl", request.model_dump())
