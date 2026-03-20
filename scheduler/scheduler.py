from apscheduler.schedulers.blocking import BlockingScheduler
from scrapers import WebCamScraper

def start_scheduler():

    scheduler = BlockingScheduler()
    web_cam = WebCamScraper(config_path="config/config.json", job_name="camera")
    take_screenshot = web_cam.scrape


    scheduler.add_job(
        take_screenshot,
        "interval",
        minutes=30,
        max_instances=1
    )
    scheduler.start()
