from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal

from ...model_service import predict_safely

router = APIRouter(prefix="/api/irrigation", tags=["irrigation"])


class IrrigationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    Soil_Type: Literal["Clay", "Loamy", "Sandy", "Silt"]
    Soil_pH: float = Field(ge=0, le=14)
    Soil_Moisture: float = Field(ge=0, le=100)
    Organic_Carbon: float = Field(ge=0, le=10)
    Electrical_Conductivity: float = Field(ge=0, le=100)
    Temperature_C: float = Field(ge=-20, le=60)
    Humidity: float = Field(ge=0, le=100)
    Rainfall_mm: float = Field(ge=0, le=10000)
    Sunlight_Hours: float = Field(ge=0, le=24)
    Wind_Speed_kmh: float = Field(ge=0, le=300)
    Crop_Type: Literal["Cotton", "Maize", "Potato", "Rice", "Sugarcane", "Wheat"]
    Crop_Growth_Stage: Literal["Flowering", "Harvest", "Sowing", "Vegetative"]
    Season: Literal["Kharif", "Rabi", "Zaid"]
    Irrigation_Type: Literal["Canal", "Drip", "Rainfed", "Sprinkler"]
    Water_Source: Literal["Groundwater", "Rainwater", "Reservoir", "River"]
    Field_Area_hectare: float = Field(gt=0, le=10000)
    Mulching_Used: Literal["No", "Yes"]
    Previous_Irrigation_mm: float = Field(ge=0, le=10000)
    Region: Literal["Central", "East", "North", "South", "West"]


@router.post("/predict")
def predict_irrigation(request: IrrigationRequest) -> dict[str, Any]:
    return predict_safely("irrigation_model.pkl", request.model_dump())
