import sys
from pathlib import Path

import pytest
import requests

# Ensure project root is on sys.path so 'scrapers' package can be imported in tests
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scrapers import weather_client


class DummyResponse:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code

    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            raise requests.HTTPError(f"status {self.status_code}")

    def json(self):
        return self._json


def test_fetch_current_weather_success(monkeypatch):
    expected_current = {
        "temperature_2m": 15.2,
        "relative_humidity_2m": 82,
        "precipitation": 0.3,
        "weather_code": 2,
        "wind_speed_10m": 4.7,
    }

    def fake_get(url, params, timeout):
        assert url == weather_client.OPEN_METEO_URL
        assert params["latitude"] == 52.0
        assert params["longitude"] == 20.0
        return DummyResponse({"current": expected_current})

    monkeypatch.setattr(weather_client.requests, "get", fake_get)

    result = weather_client.fetch_current_weather(52.0, 20.0)
    assert result == {
        "temp_c": 15.2,
        "weather_code": 2,
        "wind_speed_m_s": 4.7,
        "precipitation_mm": 0.3,
        "relative_humidity": 82,
    }


def test_fetch_current_weather_missing_temperature(monkeypatch):
    def fake_get(url, params, timeout):
        return DummyResponse({"current": {"weather_code": 3}})

    monkeypatch.setattr(weather_client.requests, "get", fake_get)

    result = weather_client.fetch_current_weather(52.0, 20.0)
    assert result is None


def test_fetch_current_weather_on_request_exception(monkeypatch):
    def fake_get(url, params, timeout):
        raise weather_client.requests.RequestException("net failure")

    monkeypatch.setattr(weather_client.requests, "get", fake_get)

    result = weather_client.fetch_current_weather(52.0, 20.0)
    assert result is None
