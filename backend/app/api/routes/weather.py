import json
import os
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from fastapi import APIRouter, HTTPException, Query

from ... import config  # noqa: F401

router = APIRouter(prefix="/api/weather", tags=["weather"])
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5"


def _request(endpoint: str, params: dict[str, str]) -> dict:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="Weather service is not configured. Set OPENWEATHER_API_KEY.",
        )

    query = urlencode({**params, "appid": api_key, "units": "metric"})
    try:
        with urlopen(f"{OPENWEATHER_URL}/{endpoint}?{query}", timeout=10) as response:
            return json.load(response)
    except HTTPError as error:
        if error.code == 401:
            raise HTTPException(
                status_code=502,
                detail="Weather provider rejected the API key. Check that the key is active and valid.",
            ) from error
        if error.code == 404:
            raise HTTPException(
                status_code=502,
                detail="Weather provider could not find the configured city.",
            ) from error
        raise HTTPException(status_code=502, detail="Weather provider request failed.") from error
    except (URLError, TimeoutError) as error:
        raise HTTPException(status_code=502, detail="Weather provider is unavailable.") from error


def _location_params(city: str | None, latitude: float | None, longitude: float | None) -> dict[str, str]:
    if latitude is not None and longitude is not None:
        return {"lat": str(latitude), "lon": str(longitude)}
    return {"q": city or os.getenv("WEATHER_CITY", "Delhi")}


@router.get("")
def get_weather(
    city: str | None = Query(default=None, min_length=1, max_length=100),
    latitude: float | None = Query(default=None, ge=-90, le=90),
    longitude: float | None = Query(default=None, ge=-180, le=180),
) -> dict:
    if (latitude is None) != (longitude is None):
        raise HTTPException(status_code=422, detail="Latitude and longitude must be provided together.")

    params = _location_params(city, latitude, longitude)
    current = _request("weather", params)
    forecast = _request("forecast", params)
    daily: dict[str, dict] = {}

    for item in forecast["list"]:
        date = datetime.fromtimestamp(item["dt"], tz=timezone.utc).date().isoformat()
        entry = daily.setdefault(
            date,
            {
                "date": date,
                "temperatures": [],
                "rain_probability": 0,
                "description": item["weather"][0]["description"].title(),
                "icon": item["weather"][0]["icon"],
            },
        )
        entry["temperatures"].append(item["main"]["temp"])
        entry["rain_probability"] = max(entry["rain_probability"], round(item.get("pop", 0) * 100))

    days = list(daily.values())[:5]
    for entry in days:
        temperatures = entry.pop("temperatures")
        entry["high"] = round(max(temperatures))
        entry["low"] = round(min(temperatures))

    return {
        "location": current.get("name", "Configured location"),
        "country": current.get("sys", {}).get("country", ""),
        "current": {
            "temperature": round(current["main"]["temp"]),
            "feels_like": round(current["main"]["feels_like"]),
            "description": current["weather"][0]["description"].title(),
            "icon": current["weather"][0]["icon"],
            "humidity": current["main"]["humidity"],
            "wind_speed": round(current["wind"].get("speed", 0) * 3.6, 1),
            "rain_probability": days[0]["rain_probability"] if days else 0,
        },
        "forecast": days,
    }
