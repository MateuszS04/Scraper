from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
from scrapers import WebCamScraper
import json

def start_scheduler():

    scheduler = BlockingScheduler()
    config_path="config/config.json"
    with open(config_path, 'r', encoding='utf-8') as f:
        config__data = json.load(f)
        delay_between_jobs=5
        current_delay=0
    
    for job_config in config__data.get('jobs', []):

        job_name=job_config.get('name')
        webcam=WebCamScraper(config_path=config_path, job_name=job_name)

        start_time = datetime.now() + timedelta(seconds=current_delay)

        scheduler.add_job(
            webcam.scrape,
            "interval",
            minutes=30,
            # seconds=60,
            max_instances=1,
            id=job_name,
            next_run_time=start_time
        )
        current_delay+=delay_between_jobs

    scheduler.start()
