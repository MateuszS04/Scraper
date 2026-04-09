import flet as ft
import threading
import pathlib
import sys
import os



ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from schedulers_threads.scheduler_thread import start_scheduler_thread, stop_scheduler_thread
from src.Gallery.GalleryOpening import get_gallery_view

def main(page: ft.Page):

    page.title = "WebCam Scraper"
    status = ft.Text(value="Status: Gotowy", size=14)
    page.window_width = 1000
    page.window_height = 700

    status.color = ft.Colors.WHITE

    def on_start_scraping(_): #start scheduler thread to scrape webcams
        try:
            status.value = "Uruchamiam scheduler..."
            page.update()
            threading.Thread(
                target=start_scheduler_thread,
                args=(status, page),
                daemon=True,  # thread will run in background and will not block the main thread
            ).start()
        except Exception as e:
            status.value = f"Błąd start: {e}"
            page.update()

    def on_stop_scraping(_): #stop scheduler thread to scrape webcams
        try:
            stop_scheduler_thread(status, page)
            status.value = "Scheduler zatrzymany"
            page.update()
        except Exception as e:
            status.value = f"Błąd stop: {e}"
            page.update()

    def build_home_view():
        return ft.View(
            route="/",
            controls=[
                ft.AppBar(title=ft.Text("WebCam Scraper"), bgcolor=ft.Colors.SURFACE),
                status,
                ft.Row(
                    [
                        ft.Button(
                            "Start Scraping",
                            on_click=on_start_scraping,
                            bgcolor=ft.Colors.BLUE_700,
                            color=ft.Colors.WHITE,
                        ),
                        ft.Button(
                            "Stop Scraping",
                            on_click=on_stop_scraping,
                            bgcolor=ft.Colors.RED_700,
                            color=ft.Colors.WHITE,
                        ),
                        ft.Button(
                            "Galeria",
                            on_click=lambda _: show_gallery(),
                            bgcolor=ft.Colors.GREEN_700,
                            color=ft.Colors.WHITE,
                        ),
                    ],
                    spacing=12,
                ),
            ],
        )

    def show_home():
        page.views.clear()
        page.views.append(build_home_view())
        page.update()

    def show_gallery():
        gallery_view = get_gallery_view(page, on_back=show_home)
        page.views.clear()
        page.views.append(gallery_view)
        page.update()

    show_home()


if __name__ == "__main__": 
    ft.app(target=main, assets_dir=".") # assets_dir is the directory where the assets are stored 
    #it lets flet to access local files like images, videos, etc.