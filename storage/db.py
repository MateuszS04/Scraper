from sqlalchemy import DateTime, Float, Integer, create_engine, Column, String, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base
from .db_config import dbConfig

DB_URLS = f"postgresql://{dbConfig.DB_USER}:{dbConfig.DB_PASSWORD}@{dbConfig.DB_HOST}:{dbConfig.DB_PORT}/{dbConfig.DB_NAME}"

engine = create_engine(DB_URLS)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()

class Screenshot(Base):
    __tablename__="screenshots"
    id=Column(Integer,primary_key=True)
    camera_name=Column(String,nullable=False)
    image_path=Column(String,nullable=False)
    created_at=Column(DateTime,nullable=False)
    weather_temp_c=Column(Float, nullable=True)
    weather_code=Column(Integer, nullable=True)
    weather_wind_speed_m_s=Column(Float, nullable=True)
    weather_precipitation_mm=Column(Float, nullable=True)
    weather_relative_humidity=Column(Integer, nullable=True)

def _ensure_screenshot_weather_columns():
    try:
        inspector = inspect(engine)
        if "screenshots" not in inspector.get_table_names():
            return
        existing = {c["name"] for c in inspector.get_columns("screenshots")}
    except Exception:
        return
    alters = []
    if "weather_temp_c" not in existing:
        alters.append("ALTER TABLE screenshots ADD COLUMN weather_temp_c DOUBLE PRECISION")
    if "weather_code" not in existing:
        alters.append("ALTER TABLE screenshots ADD COLUMN weather_code INTEGER")
    if "weather_wind_speed_m_s" not in existing:
        alters.append("ALTER TABLE screenshots ADD COLUMN weather_wind_speed_m_s DOUBLE PRECISION")
    if "weather_precipitation_mm" not in existing:
        alters.append("ALTER TABLE screenshots ADD COLUMN weather_precipitation_mm DOUBLE PRECISION")
    if "weather_relative_humidity" not in existing:
        alters.append("ALTER TABLE screenshots ADD COLUMN weather_relative_humidity INTEGER")
    if not alters:
        return
    with engine.begin() as conn:
        for stmt in alters:
            conn.execute(text(stmt))

def init_db():
    Base.metadata.create_all(bind=engine)
    _ensure_screenshot_weather_columns()

def save_screenshot(camera_name:str,image_path:str,created_at, weather=None):
    db=SessionLocal()
    try:
        kwargs = dict(
            camera_name=camera_name,
            image_path=image_path,
            created_at=created_at,
        )
        if weather:
            kwargs.update(
                weather_temp_c=weather.get("temp_c"),
                weather_code=weather.get("weather_code"),
                weather_wind_speed_m_s=weather.get("wind_speed_m_s"),
                weather_precipitation_mm=weather.get("precipitation_mm"),
                weather_relative_humidity=weather.get("relative_humidity"),
            )
        screenshot=Screenshot(**kwargs)
        db.add(screenshot)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()







