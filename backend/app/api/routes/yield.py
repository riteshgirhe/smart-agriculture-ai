from datetime import date
from typing import Any, Literal

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from ...model_service import predict_safely

router = APIRouter(prefix="/api/yield", tags=["yield"])


class YieldRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    Crop_Type: Literal["Cotton", "Groundnut", "Maize", "Onion", "Potato", "Rice", "Soybean", "Sugarcane", "Wheat"]
    Field_Size_hectares: float = Field(gt=0, le=10000)
    Planting_Date: date
    Soil_Type: Literal["Alluvial", "Chalky", "Clay", "Laterite", "Loamy", "Peaty", "Sandy", "Silty"]
    Fertilizer_Used: Literal["Ammonium Sulphate", "Biofertilizers", "Compost/Organic Manure", "DAP", "MOP", "NPK", "Urea"]
    Irrigation_Type: Literal["Drip Irrigation", "Flood Irrigation", "Furrow/Canal irrigation", "Rainfed", "Sprinkler Irrigation"]


@router.post("/predict")
def predict_yield(request: YieldRequest) -> dict[str, Any]:
    values = request.model_dump()
    values = {
        "Crop Type": values["Crop_Type"],
        "Field Size (hectares)": values["Field_Size_hectares"],
        "Planting Date": values["Planting_Date"],
        "Soil Type": values["Soil_Type"],
        "Fertilizer Used": values["Fertilizer_Used"],
        "Irrigation Type": values["Irrigation_Type"],
    }
    return predict_safely("random_forest_model.pkl", values)
