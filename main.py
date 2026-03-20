from scheduler.scheduler import start_scheduler
from storage.db import init_db

if __name__ == "__main__":
    init_db()       # if table not exist create it
    start_scheduler()



