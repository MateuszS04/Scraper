import flet as ft
import os

from src.DB.DB_connection import load_screenshots_with_weather

def get_gallery_view(page: ft.Page, on_back=None): 
    #function to get gallery view and display screenshots from database
    image_view = ft.Image(src="", width=800, height=500, fit="contain")
    loading_text = ft.Text("Wybierz zdjęcie z listy po prawej", italic=True)
    
    def set_preview(src): # function to update the preview image after clicking on the thumbnail
        image_view.src = src
        loading_text.value = f"Podgląd: {os.path.basename(src)}"
        page.update()

    records = load_screenshots_with_weather(200) # load screenshots from database
    

    preview_items = [] # list to store preview items
    if records:
        for r in records: 
            img_path = r.get("image_path")
            if not img_path or not os.path.exists(os.path.abspath(img_path)):
                continue
            
            abs_path = os.path.abspath(img_path)
            
            thumb = ft.Container( # container to store the thumbnail image
                content=ft.Image(src=abs_path, width=180, height=110, fit="contain"),
                border=ft.border.all(1, "#ccc"),
                on_click=lambda e, s=abs_path: set_preview(s), # set the preview image when the thumbnail is clicked
                tooltip="Kliknij, aby powiększyć",
            )
            
            meta = ft.Text(f"{r['camera_name']} | {r['weather']['temp_c']}°C", size=10)
            preview_items.append(ft.Column([meta, thumb], spacing=4))


    return ft.View( # return the gallery view
        route="/gallery",
        controls=[
            ft.AppBar(title=ft.Text("Galeria zrzutów"), bgcolor=ft.Colors.SURFACE),
            ft.Row([
                ft.Column([image_view], expand=True),
                ft.Column([
                    ft.Text("Lista zrzutów:"),
                    ft.Column(preview_items, scroll=ft.ScrollMode.ALWAYS, height=600)
                ], width=250)
            ], expand=True),
            ft.Button(
                "Powrót do menu",
                on_click=lambda _: on_back() if on_back else page.go("/"),
            )
        ]
    )