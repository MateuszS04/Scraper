import flet as ft
import sys
import pathlib


ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scheduler.scheduler import start_scheduler, stop_scheduler

def start_scheduler_thread(status: ft.Text, page: ft.Page):
    #function to start the scheduler thread
    try:
        start_scheduler()
    except Exception as e:
        status.value = f"Błąd scheduler: {e}"
        page.update()

def stop_scheduler_thread(status: ft.Text, page: ft.Page):
    #function to stop the scheduler thread
    try:
        stop_scheduler()
        status.value = "Scheduler zatrzymany."
    except Exception as e:
        status.value = f"Błąd zatrzymania scheduler: {e}"
    page.update()