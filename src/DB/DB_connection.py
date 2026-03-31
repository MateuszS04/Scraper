import sys
import pathlib
import flet as ft 


ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from storage.db import init_db, Screenshot, SessionLocal

