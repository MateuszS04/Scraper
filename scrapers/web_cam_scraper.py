from playwright.sync_api import sync_playwright
from datetime import datetime as _dt
import os
from scrapers.bas_scraper import BaseScraper
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
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            page.goto(self.url)
            path = self.get_image_path()
            page.screenshot(path=path)
            save_screenshot(self.name, path, _dt.now())
            browser.close()
