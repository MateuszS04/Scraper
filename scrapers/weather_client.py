
from __future__ import annotations

import logging
from typing import Any

import requests

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

logger = logging.getLogger(__name__)


def fetch_current_weather(latitude: float, longitude: float, timeout: float = 10.0) -> dict[str, Any] | None:
    """
    Returns a dict suitable for storage: temp_c, weather_code, wind_speed_m_s,
    precipitation_mm, relative_humidity (percent). Returns None on failure.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ",".join(
            [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "weather_code",
                "wind_speed_10m",
            ]
        ),
    }
    try:
        r = requests.get(OPEN_METEO_URL, params=params, timeout=timeout)
        r.raise_for_status()
        data = r.json()
        cur = data.get("current") or {}
        if "temperature_2m" not in cur:
            logger.warning("Open-Meteo response missing current.temperature_2m")
            return None
        return {
            "temp_c": float(cur["temperature_2m"]),
            "weather_code": int(cur.get("weather_code", 0)),
            "wind_speed_m_s": float(cur.get("wind_speed_10m", 0.0)),
            "precipitation_mm": float(cur.get("precipitation", 0.0)),
            "relative_humidity": int(cur["relative_humidity_2m"])
            if cur.get("relative_humidity_2m") is not None
            else None,
        }
    except (requests.RequestException, ValueError, KeyError, TypeError) as e:
        logger.warning("Weather fetch failed for lat=%s lon=%s: %s", latitude, longitude, e)
        return None
