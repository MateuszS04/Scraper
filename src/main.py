import flet as ft
import threading
import pathlib
import sys

ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from schedulers_threads.scheduler_thread import start_scheduler_thread, stop_scheduler_thread

def main(page: ft.Page):
    page.title = "WebCam Scraper"
    status = ft.Text(value="Status", size=14)
    def on_start_scraping(_):
        status.value = "Uruchamiam scheduler..."
        page.update()
        threading.Thread(target=start_scheduler_thread, args=(status, page), daemon=True).start()
    
    def stop_scraping(_):
        status.value = "Zatrzymuję scheduler..."
        page.update()
        threading.Thread(target=stop_scheduler_thread, args=(status, page), daemon=True).start()
        

    page.add(
        status,
        ft.Row([
            ft.ElevatedButton("Start Scraping", on_click=on_start_scraping),
            ft.ElevatedButton("Stop Scraping", on_click=stop_scraping),
            # ft.ElevatedButton("Database", on_click=on_load_screenshots),
        ])
    )



ft.run(main)