import time
import schedule
from youtube_scraper import scan_channels
from database import Session, Video

def job():
    print("Running scheduled scan...")
    scan_channels()
    # Add step to run analyzer on un-analyzed videos here

# Run every 3 hours
schedule.every(3).hours.do(job)

if __name__ == "__main__":
    print("Starting background scheduler...")
    job() # Run once on startup
    while True:
        schedule.run_pending()
        time.sleep(60)
