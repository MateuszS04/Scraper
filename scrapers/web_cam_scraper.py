from playwright.sync_api import sync_playwright
from datetime import datetime as _dt
import os
from scrapers.bas_scraper import BaseScraper
from scrapers.weather_client import fetch_current_weather
from storage.db import save_screenshot


class WebCamScraper(BaseScraper):

    def __init__(self, config_path=None, job_name=None, name=None, url=None):
        super().__init__(config_path=config_path, job_name=job_name, name=name, url=url)

    def get_image_path(self):
        os.makedirs('screenshots', exist_ok=True)
        timestamp = _dt.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.name}_{timestamp}.png"
        return os.path.join('screenshots', filename)

    def scrape(self):
        try:    
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()

                page.goto(self.url)
                try:
                    page.add_style_tag(content="#plugin-consent { display: none !important; }")
                    page.wait_for_timeout(2000)  
                except Exception as e:
                    print(f"Error handling consent popup: {e}")
                    pass    

                containner_locator = page.locator('.webcam-container')
                containner_locator.wait_for(state='visible', timeout=15000)
                path = self.get_image_path()
                containner_locator.screenshot(path=path)
                now = _dt.now()
                weather = None
                if self.latitude is not None and self.longitude is not None:
                    weather = fetch_current_weather(self.latitude, self.longitude)
                save_screenshot(self.name, path, now, weather=weather)
                browser.close()
        except Exception as e:
            print(f"Error scraping {self.name}: {e}")

