import sys
import pathlib
import flet as ft 


ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from storage.db import init_db, Screenshot, SessionLocal


def connect_db():
    init_db()
    return SessionLocal()


def load_screenshots(limit: int = 100):
    session = connect_db()
    try:
        return (
            session.query(Screenshot)
            .order_by(Screenshot.created_at.desc())
            .limit(limit)
            .all()
        )
    finally:
        session.close()


def load_screenshots_with_weather(limit: int = 100):
    """Load screenshot metadata + weather data from DB."""
    session = connect_db()
    try:
        records = (
            session.query(Screenshot)
            .order_by(Screenshot.created_at.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "id": r.id,
                "camera_name": r.camera_name,
                "image_path": r.image_path,
                "created_at": r.created_at,
                "weather": {
                    "temp_c": r.weather_temp_c,
                    "weather_code": r.weather_code,
                    "wind_speed_m_s": r.weather_wind_speed_m_s,
                    "precipitation_mm": r.weather_precipitation_mm,
                    "relative_humidity": r.weather_relative_humidity,
                },
            }
            for r in records
        ]
    finally:
        session.close()

