from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from ...model_service import predict_safely

router = APIRouter(prefix="/api/crop", tags=["crop"])


class CropRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    N: float = Field(ge=0, le=200)
    P: float = Field(ge=0, le=200)
    K: float = Field(ge=0, le=200)
    temperature: float = Field(ge=-20, le=60)
    humidity: float = Field(ge=0, le=100)
    ph: float = Field(ge=0, le=14)
    rainfall: float = Field(ge=0, le=10000)


@router.post("/recommend")
def recommend_crop(request: CropRequest) -> dict[str, Any]:
    return predict_safely("crop_recommendation_model.pkl", request.model_dump())
