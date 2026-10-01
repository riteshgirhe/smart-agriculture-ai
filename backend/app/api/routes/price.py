from datetime import date
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from ...model_service import predict_safely

router = APIRouter(prefix="/api/price", tags=["price"])


class PriceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    month: date
    commodity_name: str = Field(min_length=1, max_length=80)
    state_name: str = Field(min_length=1, max_length=80)
    district_name: str = Field(min_length=1, max_length=80)
    avg_min_price: float = Field(ge=0)
    avg_max_price: float = Field(ge=0)
    calculationType: str = Field(min_length=1, max_length=40)
    change: float = Field(ge=-100000, le=100000)


@router.post("/predict")
def predict_price(request: PriceRequest) -> dict[str, Any]:
    return predict_safely("price_prediction_model.pkl", request.model_dump())
