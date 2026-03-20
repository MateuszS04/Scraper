from abc import ABC, abstractmethod
import json

class BaseScraper(ABC):

    def __init__(self, config_path=None, job_name=None, name=None, url=None):
        if config_path and job_name:
            with open(config_path, 'r') as f: #getting config for camras from config file in json format
                cfg = json.load(f)
            jobs = cfg.get('jobs', [])
            job_cfg = next((j for j in jobs if j.get('name') == job_name), None)
            if not job_cfg:
                raise ValueError(f"Job '{job_name}' not found in config '{config_path}'")
            self.name = job_cfg.get('name')
            self.url = job_cfg.get('url')
        else:
            if name is None or url is None:
                raise ValueError('Either config_path+job_name or name+url must be provided')
            self.name = name
            self.url = url

    @abstractmethod
    def scrape(self):
        pass