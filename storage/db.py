from sqlalchemy import DateTime, create_engine, Column, Integer, String
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

def init_db():
    Base.metadata.create_all(bind=engine)

def save_screenshot(camera_name:str,image_path:str,created_at):
    db=SessionLocal()
    try:
        screenshot=Screenshot(
            camera_name=camera_name,
            image_path=image_path,
            created_at=created_at)
        db.add(screenshot)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()







